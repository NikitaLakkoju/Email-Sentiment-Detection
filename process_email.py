import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email import policy
import requests
import json
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
from email.utils import parseaddr

# ✅ Load environment variables
load_dotenv()

# -------------------------------
# 1. Email Account Configuration
# create an .env file to store all your personal information of sql and gmail
# -------------------------------
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# -------------------------------
# 2. Sentiment-based Routing
# -------------------------------
POSITIVE_TO = "xxxxu@gmail.com" #add your emails here 
NEGATIVE_TO = "xxxxu@gmail.com"
NEUTRAL_TO  = "xxxx@gmail.com"

# -------------------------------
# 3. MySQL Database Connection
# -------------------------------
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE") #sql password and database would be taken from the .env file
    )

def save_email_to_mysql(sender, subject, body, sentiment, highlighted_body):
    """Store the processed email into the MySQL database."""
    conn = get_mysql_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO emails (sender, subject, body, sentiment, highlighted_body, received_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (sender, subject, body, sentiment, highlighted_body, datetime.now()))
    conn.commit()
    conn.close()

# -------------------------------
# 4. Fetch Latest UNREAD Email
# -------------------------------
def fetch_latest_email():
    """Connects to Gmail and fetches the latest unread email."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        if not email_ids:
            print("📭 No new unread emails.")
            return None, None, None

        latest_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email, policy=policy.default)

        subject = str(msg["subject"])
        name, sender_email = parseaddr(msg["from"])
        sender = f"{name} <{sender_email}>"

        body_part = msg.get_body(preferencelist=('plain', 'html'))
        if body_part:
            body = body_part.get_content()
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')

        return subject, sender, body

    except Exception as e:
        print("❌ Error fetching email:", str(e))
        return None, None, None

# -------------------------------
# 5. Get Sentiment + Highlights
# -------------------------------
def get_sentiment_and_highlights(text):
    """Sends email content to local Ollama LLM and returns sentiment and highlighted keywords."""
    prompt = f"""
Classify the sentiment of this email as Positive, Negative, or Neutral.
Also highlight the key words/phrases in the email that influenced your decision.

Respond ONLY in this JSON format:
{{
  "sentiment": "positive | negative | neutral",
  "highlights": ["word1", "word2"]
}}

Email:
\"\"\"
{text}
\"\"\"
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False}
        )

        if res.status_code != 200:
            print(f"❌ Ollama LLM Error: HTTP {res.status_code}")
            return "neutral", text

        response_json = res.json().get("response", "")

        try:
            result = json.loads(response_json)
            sentiment = result["sentiment"].lower()
            highlights = result.get("highlights", [])

            highlighted_body = text
            for word in highlights:
                highlighted_body = highlighted_body.replace(word, f"<mark>{word}</mark>")

            return sentiment, highlighted_body

        except json.JSONDecodeError:
            print("⚠️ LLM returned invalid JSON. Fallback to 'neutral'")
            print("Response was:", response_json)
            return "neutral", text

    except Exception as e:
        print("❌ Error connecting to Ollama:", str(e))
        return "neutral", text
# -------------------------------
# 6. Forward Email by Sentiment
# -------------------------------
def forward_email(subject, highlighted_body, sentiment):
    """Forwards email to appropriate address based on sentiment."""
    if "positive" in sentiment:
        to_email = POSITIVE_TO
    elif "negative" in sentiment:
        to_email = NEGATIVE_TO
    else:
        to_email = NEUTRAL_TO

    msg = MIMEText(highlighted_body, "html")
    msg["Subject"] = f"[Forwarded Based on Sentiment] {subject}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"📤 Forwarded email to {to_email} based on sentiment: {sentiment.capitalize()}")
    except Exception as e:
        print("❌ Error forwarding email:", str(e))


# -------------------------------
# 7. Main Program Flow
# -------------------------------
def main():
    subject, sender, body = fetch_latest_email()
    if body:
        print(f"✉️ New email from: {sender}")
        print("🔍 Analyzing sentiment...")
        sentiment, highlighted_body = get_sentiment_and_highlights(body)


        print(f"🧠 Sentiment Detected: {sentiment}")
        forward_email(subject, highlighted_body, sentiment)
        save_email_to_mysql(sender, subject, body, sentiment, highlighted_body)
    else:
        print("✅ No action needed.")

# Entry point for both standalone and background execution
if __name__ == "__main__":
    main()
