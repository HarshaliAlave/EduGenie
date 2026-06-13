# 🧞 EduGenie – AI Study Companion
### Full-Stack Mini Project | Computer Engineering | YBIT 2025–26

---

## 📁 Project Structure

```
edugenie/
├── app.py                   ← Flask backend (all routes)
├── schema.sql               ← MySQL database schema
├── requirements.txt         ← Python dependencies
├── uploads/                 ← Uploaded PDFs (auto-created)
├── templates/
│   ├── base.html            ← Shared navbar/footer layout
│   ├── index.html           ← Landing page
│   ├── login.html           ← Login page
│   ├── register.html        ← Register page
│   ├── dashboard.html       ← Main dashboard + upload
│   ├── document.html        ← Per-document actions
│   ├── summary.html         ← AI study notes
│   ├── quiz.html            ← Interactive MCQ quiz
│   ├── results.html         ← Quiz results & review
│   ├── chatbot.html         ← Doubt-solving chatbot
│   └── analytics.html       ← Score analytics
└── static/
    ├── css/style.css        ← Full stylesheet (dark theme)
    └── js/
        ├── main.js          ← Flash messages, form loading
        └── upload.js        ← Drag & drop file upload
```

---

## ⚙️ Setup Instructions

### Step 1 – Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 2 – Set up MySQL database
Open MySQL Workbench and run:
```bash
mysql -u root -p < schema.sql
```
This creates the `edugenie_db` database with all required tables.

### Step 3 – Configure your credentials in `app.py`

Open `app.py` and update these 4 lines:

```python
# Line ~19: Gemini API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Lines ~24–27: MySQL credentials
host="your_remote_host",
user="your_username",
password="your_password",
database="edugenie_db"
```

**Getting Gemini API Key:**
- Go to https://aistudio.google.com/app/apikey
- Create a free API key
- Paste it into app.py

### Step 4 – Run the application
```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## 🗄️ Database Schema (ERD Summary)

```
Users          Documents          Quizzes
─────────      ──────────────     ────────────
user_id   ←── user_id            quiz_id
username       doc_id        ←── doc_id
email          file_name          score
password_hash  extracted_text     total_questions
created_at     upload_timestamp   taken_at
```

---

## 🌐 Application Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page |
| `/register` | GET/POST | User registration |
| `/login` | GET/POST | User login |
| `/logout` | GET | Logout |
| `/dashboard` | GET | Main dashboard |
| `/upload` | POST | Upload & process PDF |
| `/document/<id>` | GET | View document actions |
| `/summarize/<id>` | POST | Generate AI study notes |
| `/generate_quiz/<id>` | POST | Generate MCQ quiz |
| `/submit_quiz` | POST | Submit quiz & save score |
| `/chatbot/<id>` | GET/POST | Doubt-solving chatbot |
| `/analytics` | GET | Score analytics |

---

## 🔧 Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, Flask |
| Database | MySQL (remote) |
| AI Engine | Google Gemini 1.5 Pro API |
| PDF Processing | PyPDF2 |
| Templating | Jinja2 (Server-Side Rendering) |

> ⚠️ No JSON, No Node.js, No React — pure HTML form submissions with SSR

---

## 👥 Team

- Alave Harshali Sushant (CE02)
- Dabholkar Amruta Anand (CE09)
- Mulla Juveriya Kutubuddin (CE62)
- Kadam Sanjal Balaji (CE36)

**Guide:** Prof. Mrs. S.S. Naik  
**Department:** Computer Engineering  
**Institute:** Yashwantrao Bhonsale Institute of Technology  
**Academic Year:** 2025–26
