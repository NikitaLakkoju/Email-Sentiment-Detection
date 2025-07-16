# Email Sentiment Detection (Gemma 2B vs Yi 9B - Local LLMs via Ollama)

This project performs sentiment analysis on incoming Gmail emails using **two local LLMs (Gemma 2B and Yi 9B)** via [Ollama](https://ollama.com/), and routes emails accordingly based on sentiment (positive, negative, neutral). It stores the results in a MySQL database and displays them in an interactive Flask dashboard.


🔍 FEATURES: 

- 📬 Fetch unread Gmail emails
- 🧠 Use **Gemma 2B** and **Yi 9B** via Ollama to classify sentiment
- ⚖️ Compare model performance and highlight influencing keywords
- 📊 Interactive Flask dashboard (filter by sentiment, sender, date)
- 🗂 MySQL database for full email + sentiment history
- 📤 Forward emails based on sentiment to different teams

---------------

🧪 MODEL COMPARISON: 

This project supports **running both LLMs (Gemma 2B and Yi 9B)** on the same emails for comparison.  
Observations:
- **Yi 9B** tends to highlight more sentiment-driving keywords but sometimes over-labels.
- **Gemma 2B** is more conservative but more consistent in sentiment labeling.

---------------

⚙️ PROJECT ARCHITECTURE: 

📦 email_sentiment_dashboard_v2/
├── templates/
│   └── dashboard.html       # Frontend UI for the dashboard (HTML + Chart.js)
├── venv/                    # Python virtual environment (excluded from Git)
├── .env                     # Environment variables (e.g., DB credentials)
├── app.py                   # Flask backend to serve the dashboard
├── database.sql             # SQL file to create the `emails` table
├── fetch_loop.py            # Script to fetch, analyze, and store new emails
├── process_email.py         # Core logic: LLM (Gemma/Yi) based sentiment + keyword highlight
├── requirements.txt         # Python dependencies list (Flask, mysql-connector, etc.)


---------------

🧩 SETUP:


- Project folder: email_sentiment_dashboard_v2
Python virtual environment (venv) is located in the project folder.

You have the following Python scripts:
- fetch_loop.py → fetches unread emails
- app.py → runs the Flask dashboard

  
MySQL is already running (locally)
Ollama is already running and listening (Gemma or Yi model is pulled)

---------------

FINAL STEPS:

You need to
- Activate the virtual environment
- Run the fetcher loop
- Launch the Flask dashboard

---------------

📄 License
This project is licensed under the Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).

© 2025 Nikita Lakkoju. All rights reserved.
