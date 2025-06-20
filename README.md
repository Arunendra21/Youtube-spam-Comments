# 📌 YouTube Spam Comment Detector

A simple and beginner-friendly Streamlit web app that detects spam comments from any public YouTube video.  
Just paste the YouTube video link or ID, and the app fetches comments, checks for spam using common spam keywords, and displays the results — no coding required!

---

## 🎯 Features

- 🔗 Paste any YouTube video link or ID
- 🔍 Fetches comments using YouTube Data API v3
- 🧠 Detects spam comments using a rule-based filter
- 📂 Download the detected spam comments as a CSV file
- 💻 Clean and minimal web interface with Streamlit

---

## 🛠️ Built With

- Python
- Streamlit
- Pandas
- Requests
- YouTube Data API v3

---

## 📦 Installation (For Developers)

```bash
git clone https://github.com/your-username/youtube-spam-detector.git
cd youtube-spam-detector
pip install -r requirements.txt
streamlit run app.py
