# Copyright 2026 Harshali Alave
# EduGenie - AI Study Companion
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
#
# Original web application hosted on PythonAnywhere
# Unauthorized copying or redistribution is prohibited.
import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import PyPDF2
from google import genai

app = Flask(__name__)
app.secret_key = 'edugenie_secret_key_2025'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ─── Gemini API Configuration ────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDcb25h4AD7LRHkcTnlF_N3ap00g2ETMsc"  # ← Paste your NEW API key here
client = genai.Client(api_key=GEMINI_API_KEY)

# ─── Database Connection ─────────────────────────────────────────────────────
def get_db_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="2Snbm78ZCkMuPsj.root",
        password="DzATxnpRmb5Ivp33",
        database="test",
        ssl_ca="ca.pem",
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )

# ─── Gemini Helper ────────────────────────────────────────────────────────────
def ask_gemini(prompt):
    # Models confirmed available from your account
    models_to_try = [
        "models/gemini-2.5-flash",
        "models/gemini-2.0-flash",
        "models/gemini-2.0-flash-lite",
        "models/gemini-flash-latest",
        "models/gemini-2.5-pro",
    ]
    errors = []
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            errors.append(f"{model_name}: {str(e)[:80]}")
            continue
    error_summary = " | ".join(errors[:2])
    return f"AI Error: {error_summary}. Please create a new API key at aistudio.google.com/app/apikey"

# ─── PDF Text Extraction ──────────────────────────────────────────────────────
def extract_text_from_pdf(filepath):
    extracted_text = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
    return extracted_text

# ════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')

# ─── Register ────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email    = request.form['email'].strip()
        password = request.form['password']
        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Email already registered. Please login.', 'error')
            cursor.close(); conn.close()
            return redirect(url_for('register'))
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        conn.commit()
        cursor.close(); conn.close()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# ─── Login ────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip()
        password = request.form['password']
        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM Users WHERE email = %s AND password_hash = %s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close(); conn.close()
        if user:
            session['user_id']  = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try again.', 'error')
    return render_template('login.html')

# ─── Logout ───────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ─── Dashboard ────────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT d.doc_id, d.file_name, d.upload_timestamp FROM Documents d WHERE d.user_id = %s ORDER BY d.upload_timestamp DESC",
        (session['user_id'],)
    )
    documents = cursor.fetchall()
    cursor.execute(
        """SELECT q.quiz_id, q.score, q.total_questions, d.file_name
           FROM Quizzes q JOIN Documents d ON q.doc_id = d.doc_id
           WHERE d.user_id = %s ORDER BY q.quiz_id DESC LIMIT 5""",
        (session['user_id'],)
    )
    recent_scores = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template('dashboard.html', documents=documents, recent_scores=recent_scores)

# ─── Upload PDF ───────────────────────────────────────────────────────────────
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if 'pdf_file' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('dashboard'))
    file = request.files['pdf_file']
    if file.filename == '' or not file.filename.endswith('.pdf'):
        flash('Please upload a valid PDF file.', 'error')
        return redirect(url_for('dashboard'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    extracted_text = extract_text_from_pdf(filepath)
    conn   = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Documents (user_id, file_name, extracted_text) VALUES (%s, %s, %s)",
        (session['user_id'], file.filename, extracted_text)
    )
    conn.commit()
    doc_id = cursor.lastrowid
    cursor.close(); conn.close()
    flash('PDF uploaded and processed successfully!', 'success')
    return redirect(url_for('document_view', doc_id=doc_id))

# ─── Document View ────────────────────────────────────────────────────────────
@app.route('/document/<int:doc_id>')
def document_view(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Documents WHERE doc_id = %s AND user_id = %s",
                   (doc_id, session['user_id']))
    doc = cursor.fetchone()
    cursor.close(); conn.close()
    if not doc:
        flash('Document not found.', 'error')
        return redirect(url_for('dashboard'))
    return render_template('document.html', doc=doc)

# ─── Summarize ────────────────────────────────────────────────────────────────
@app.route('/summarize/<int:doc_id>', methods=['POST'])
def summarize(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT extracted_text, file_name FROM Documents WHERE doc_id = %s AND user_id = %s",
                   (doc_id, session['user_id']))
    doc = cursor.fetchone()
    cursor.close(); conn.close()
    if not doc:
        flash('Document not found.', 'error')
        return redirect(url_for('dashboard'))
    prompt = (
        "You are an expert academic tutor. Generate detailed, well-structured study notes from the textbook content below.\n"
        "Follow this EXACT formatting style:\n\n"
        "## Chapter Title\n"
        "Brief 2-3 line overview of the chapter.\n\n"
        "---\n\n"
        "### ➢ Topic Name\n"
        "**Definition:** Clear one-line definition of the topic.\n\n"
        "Brief explanation paragraph.\n\n"
        "**Key Points:**\n"
        "- Point 1\n"
        "- Point 2\n"
        "- Point 3\n\n"
        "**Techniques / Types / Components** (if applicable):\n"
        "- **Term 1** - explanation\n"
        "- **Term 2** - explanation\n\n"
        "**Example:** Real-world example in one line.\n\n"
        "---\n\n"
        "Repeat the above pattern for EVERY topic in the content.\n"
        "At the end, add:\n\n"
        "## 📌 Key Takeaways\n"
        "- Most important point 1\n"
        "- Most important point 2\n"
        "- Most important point 3\n\n"
        "## 🎯 Exam Tips\n"
        "- Likely exam question 1\n"
        "- Likely exam question 2\n"
        "- Likely exam question 3\n\n"
        "## 📊 Quick Revision Table\n"
        "| Term | Meaning |\n"
        "| --- | --- |\n"
        "| term1 | meaning1 |\n"
        "| term2 | meaning2 |\n\n"
        "IMPORTANT RULES:\n"
        "- Cover EVERY topic from the content, do not skip anything\n"
        "- Use simple English a student can easily understand\n"
        "- Be detailed under each topic\n"
        "- Always add Examples for every concept\n\n"
        "Textbook Content:\n\n"
        + doc['extracted_text'][:15000]
    )
    summary = ask_gemini(prompt)
    return render_template('summary.html', summary=summary, doc_id=doc_id, filename=doc['file_name'])

# ─── Generate Quiz ────────────────────────────────────────────────────────────
@app.route('/generate_quiz/<int:doc_id>', methods=['POST'])
def generate_quiz(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn   = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT extracted_text, file_name FROM Documents WHERE doc_id = %s AND user_id = %s",
                   (doc_id, session['user_id']))
    doc = cursor.fetchone()
    cursor.close(); conn.close()
    if not doc:
        flash('Document not found.', 'error')
        return redirect(url_for('dashboard'))
    prompt = (
        "Generate exactly 5 multiple-choice questions from the following textbook content. "
        "Format each question STRICTLY like this:\n\n"
        "Q1: [Question text]\n"
        "A) [Option]\nB) [Option]\nC) [Option]\nD) [Option]\n"
        "ANSWER: [A/B/C/D]\n\n"
        "Repeat for Q2 through Q5. Do not add any other text.\n\n"
        + doc['extracted_text'][:12000]
    )
    raw = ask_gemini(prompt)
    questions = []
    blocks = re.split(r'\nQ\d+:', '\nQ1:' + raw.split('Q1:',1)[-1] if 'Q1:' in raw else raw)
    for block in blocks:
        if not block.strip(): continue
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if len(lines) < 6: continue
        q_text = lines[0]; options = {}; answer = ''
        for line in lines[1:]:
            if line.startswith('A)'):        options['A'] = line[2:].strip()
            elif line.startswith('B)'):      options['B'] = line[2:].strip()
            elif line.startswith('C)'):      options['C'] = line[2:].strip()
            elif line.startswith('D)'):      options['D'] = line[2:].strip()
            elif line.startswith('ANSWER:'): answer = line.replace('ANSWER:','').strip()
        if len(options) == 4 and answer:
            questions.append({'question': q_text, 'options': options, 'answer': answer})
    return render_template('quiz.html', questions=questions, doc_id=doc_id, filename=doc['file_name'])

# ─── Submit Quiz ──────────────────────────────────────────────────────────────
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doc_id = int(request.form['doc_id'])
    total  = int(request.form['total_questions'])
    correct_answers = {}; user_answers = {}
    for key, val in request.form.items():
        if key.startswith('correct_'):
            correct_answers[key.replace('correct_', '')] = val
        elif key.startswith('answer_'):
            user_answers[key.replace('answer_', '')] = val
    score = 0; results = []
    for idx in correct_answers:
        correct = correct_answers[idx]; chosen = user_answers.get(idx, '')
        is_correct = chosen == correct
        if is_correct: score += 1
        results.append({'index': idx, 'correct': correct, 'chosen': chosen, 'is_correct': is_correct})
    conn   = get_db_connection(); cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Quizzes (doc_id, score, total_questions) VALUES (%s, %s, %s)",
        (doc_id, score, total)
    )
    conn.commit(); cursor.close(); conn.close()
    return render_template('results.html', score=score, total=total, results=results, doc_id=doc_id)

# ─── Chatbot ──────────────────────────────────────────────────────────────────
@app.route('/chatbot/<int:doc_id>', methods=['GET', 'POST'])
def chatbot(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn   = get_db_connection(); cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT extracted_text, file_name FROM Documents WHERE doc_id = %s AND user_id = %s",
                   (doc_id, session['user_id']))
    doc = cursor.fetchone(); cursor.close(); conn.close()
    if not doc:
        flash('Document not found.', 'error')
        return redirect(url_for('dashboard'))
    answer = None; question = None
    if request.method == 'POST':
        question = request.form['question'].strip()
        full_text = doc['extracted_text'][:20000]
        prompt = (
            "You are EduGenie, a friendly AI study assistant. "
            "Answer the student question based on the textbook content. "
            "Rules: "
            "1. Answer clearly and in detail. "
            "2. Use bullet points when helpful. "
            "3. Give examples if possible. "
            "4. If not in the text use general knowledge and mention it. "
            "5. Always try your best to answer, never refuse.\n\n"
            "Textbook Content:\n" + full_text + "\n\n"
            "Student Question: " + question + "\n\n"
            "Provide a helpful detailed answer:"
        )
        answer = ask_gemini(prompt)
    return render_template('chatbot.html', doc=doc, doc_id=doc_id, question=question, answer=answer)

# ─── Analytics ────────────────────────────────────────────────────────────────
@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn   = get_db_connection(); cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT q.quiz_id, q.score, q.total_questions,
                  ROUND(q.score * 100.0 / q.total_questions, 1) AS percentage, d.file_name
           FROM Quizzes q JOIN Documents d ON q.doc_id = d.doc_id
           WHERE d.user_id = %s ORDER BY q.quiz_id ASC""",
        (session['user_id'],)
    )
    scores = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) AS total_docs FROM Documents WHERE user_id = %s", (session['user_id'],))
    total_docs = cursor.fetchone()['total_docs']
    cursor.execute(
        """SELECT ROUND(AVG(q.score * 100.0 / q.total_questions), 1) AS avg_score
           FROM Quizzes q JOIN Documents d ON q.doc_id = d.doc_id WHERE d.user_id = %s""",
        (session['user_id'],)
    )
    avg_result = cursor.fetchone()
    avg_score  = avg_result['avg_score'] if avg_result['avg_score'] else 0
    cursor.close(); conn.close()
    return render_template('analytics.html', scores=scores, total_docs=total_docs, avg_score=avg_score)

if __name__ == '__main__':
    app.run(debug=True)
