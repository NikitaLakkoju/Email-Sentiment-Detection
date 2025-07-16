# Email Sentiment Detection (Gemma 2B vs Yi 9B - Local LLMs via Ollama)

This project performs sentiment analysis on incoming Gmail emails using **two local LLMs (Gemma 2B and Yi 9B)** via [Ollama](https://ollama.com/), and routes emails accordingly based on sentiment (positive, negative, neutral). It stores the results in a MySQL database and displays them in an interactive Flask dashboard.

🔍 Features

- 📬 Fetch unread Gmail emails
- 🧠 Use **Gemma 2B** and **Yi 9B** via Ollama to classify sentiment
- ⚖️ Compare model performance and highlight influencing keywords
- 📊 Interactive Flask dashboard (filter by sentiment, sender, date)
- 🗂 MySQL database for full email + sentiment history
- 📤 Forward emails based on sentiment to different teams

🧪 Model Comparison

This project supports **running both LLMs (Gemma 2B and Yi 9B)** on the same emails for comparison.  
Observations:
- **Yi 9B** tends to highlight more sentiment-driving keywords but sometimes over-labels.
- **Gemma 2B** is more conservative but more consistent in sentiment labeling.
