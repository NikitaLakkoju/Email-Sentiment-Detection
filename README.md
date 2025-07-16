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

<pre> ```text 📦 email_sentiment_dashboard_v2/ ├── templates/ # HTML templates for Flask │ └── dashboard.html # Interactive dashboard UI ├── venv/ # Python virtual environment (not pushed to GitHub) ├── .env # Environment variables (DB creds, secret keys) ├── app.py # Flask server to render the dashboard and handle routes ├── database.sql # MySQL schema for storing emails and sentiments ├── fetch_loop.py # Script to fetch and classify new emails using LLMs ├── process_email.py # LLM prompt logic, sentiment classification & keyword highlighting ├── requirements.txt # All Python dependencies for the project ``` </pre>

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
