# 🧞 EduGenie – AI Study Companion

An AI-powered study companion built with Flask and Google Gemini that helps students generate study notes, take quizzes, and solve doubts from uploaded PDF textbooks.

---

## 📁 Project Structure

```
edugenie/
├── app.py                ← Flask backend
├── schema.sql            ← MySQL database schema
├── requirements.txt      ← Python dependencies
├── uploads/              ← Uploaded PDFs (auto-created)
├── templates/            ← HTML pages
└── static/               ← CSS and JS files
```

---

## ⚙️ Setup Instructions

### Step 1 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 – Setup MySQL database
Run in MySQL Workbench:
```sql
source schema.sql
```

### Step 3 – Configure credentials in app.py
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="edugenie_db"
    )
```

### Step 4 – Run
```bash
python app.py
```
Open: **http://127.0.0.1:5000**

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3, Flask |
| Database | MySQL |
| AI Engine | Google Gemini API |
| PDF Processing | PyPDF2 |
| Templating | Jinja2 |

---

## 🌐 Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/register` | GET/POST | Register |
| `/login` | GET/POST | Login |
| `/dashboard` | GET | Dashboard |
| `/upload` | POST | Upload PDF |
| `/summarize/<id>` | POST | AI study notes |
| `/generate_quiz/<id>` | POST | MCQ quiz |
| `/submit_quiz` | POST | Submit quiz |
| `/chatbot/<id>` | GET/POST | Doubt solver |
| `/analytics` | GET | Analytics |

---

## 🗄️ Database Schema

```
Users ──── Documents ──── Quizzes
```

---

## 📌 Notes
- Get free Gemini API key at: https://aistudio.google.com/app/apikey
- MySQL must be running before starting the app
- PDFs are stored locally in the uploads/ folder