import streamlit as st
import requests
import sqlite3
import hashlib 
from io import BytesIO 
from pymongo import MongoClient 


# Page Title
st.markdown("""
<h1 style='color:#f9fafb;'>🚀 AI Interview Prep </h1>
""", unsafe_allow_html=True)

# CSS
st.markdown("""
<style>
div[data-testid="stTabs"] {
    background-color: #111827;
    padding: 10px;
    border-radius: 15px;
}
button[data-baseweb="tab"] {
    background-color: #1f2937;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    margin: 5px;
    border: 1px solid #374151;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #38bdf8;
    color: black;
    font-weight: bold;
}
div[data-testid="stTabsPanel"] {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# MongoDB Connection
# =========================
client_mongo = MongoClient("mongodb://localhost:27017/")
db = client_mongo["ai_interview_prep"]
users_collection = db["users"]
interview_collection = db["interviews"]

# =========================
# 🌐 CONFIG
# =========================
st.set_page_config(page_title="AI Interview Prep", layout="wide")


from groq import Groq

client = Groq(api_key="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")
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Give 5 interview questions with answers for {role}"
        }
    ]
)
# 🗄️ DATABASE (PUT HERE)
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

import streamlit as st

st.set_page_config(page_title="AI Interview Prep", layout="wide")

# =========================
# 🔐 SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

import streamlit as st
import sqlite3
import hashlib

# =========================
# 🗄️ DATABASE SETUP
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# =========================
# 🔐 HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
# =========================
# DATABASE FUNCTIONS
# =========================

def register_user(username, password):
    users_collection.insert_one({
        "username": username,
        "password": password
    })

def login_user(username, password):
    return users_collection.find_one({
        "username": username,
        "password": password
    })

def save_interview(username, questions, answers, score):
    interview_collection.insert_one({
        "username": username,
        "questions": questions,
        "answers": answers,
        "score": score
    })

# =========================
# 🆕 REGISTER USER
# =========================
def register_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

# =========================
# 🔑 LOGIN CHECK
# =========================
def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()
st.markdown("""

### 💡 Crack Interviews with AI-powered Practice
""")

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.success(f"Welcome back, {st.session_state.user} 👋")
    st.info("Keep practicing daily to improve your interview score 🚀")

# =========================
# 🔐 AUTH PAGE
# =========================
def auth_page():
    st.title("Login System")

    menu = st.radio("Choose Option", ["Login", "Register"])

    # ================= REGISTER =================
    if menu == "Register":
        st.subheader("🆕 Create New Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created successfully 🎉")
            else:
                st.error("Username already exists ❌")

    # ================= LOGIN =================
    if menu == "Login":
        st.subheader("🔐 Login to Continue")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful 🚀")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

# =========================
# 🚫 BLOCK UNTIL LOGIN
# =========================
if not st.session_state.logged_in:
    auth_page()
    st.stop()

# =========================
# 🏠 DASHBOARD AFTER LOGIN
# =========================
st.sidebar.title("👤 User Panel")

# User info card
st.sidebar.markdown(f"""
### 👋 Hello, {st.session_state.user}

🟢 Status: Active Learner  
🎯 Goal: Crack Interviews  
📅 Today: Practice Mode

---
""")

# Quick stats (you can later connect DB)
st.sidebar.metric("📄 Tests Taken", 5)
st.sidebar.metric("🎤 Mock Interviews", 3)
st.sidebar.metric("📊 Avg Score", "7.8/10")

st.sidebar.markdown("---")

# Navigation shortcuts
st.sidebar.markdown("### ⚡ Quick Actions")
st.sidebar.write("• Generate Questions")
st.sidebar.write("• Start Mock Interview")
st.sidebar.write("• Improve Resume")
st.sidebar.write("• Check Analytics")

st.sidebar.markdown("---")

# Progress bar (fake but impressive UI)
st.sidebar.markdown("### 📈 Preparation Progress")
st.sidebar.progress(0.65)
st.sidebar.caption("65% Ready for Interviews 🚀")

st.sidebar.markdown("---")

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# =========================
# 📑 TABS
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Questions",
    "🎤 Mock Interview",
    "📝 Resume Builder",
    "📊 Resume Analyzer",
    "📚 Study Plan",
    "📈 Analytics"
])

# =========================
# 📄 TAB 1 - QUESTIONS
# =========================
with tab1:
    st.header("Interview Questions Generator")

role = st.text_input("Enter Job Role")

if st.button("Generate Questions"):
    if role.strip() == "":
        st.warning("Enter role")
    else:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"Give 5 interview questions with answers for {role}"
                }
            ]
        )

        st.write(response.choices[0].message.content)
# =========================
# 🎤 TAB 2 - MOCK INTERVIEW
# =========================
with tab2:
    st.header("🎤 Mock Interview")

    # Initialize session state
    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.index = 0

    # Start Interview
    if st.button("Start Interview", key="start_mock"):
        with st.spinner("Generating questions..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": """
Generate 5 interview questions for a software developer.
Return ONLY questions in numbered format like:
1. ...
2. ...
3. ...
4. ...
5. ...
"""
                    }
                ]
            )

        text = response.choices[0].message.content

        # Convert response into clean list
        questions = text.split("\n")
        questions = [q.strip() for q in questions if q.strip() != ""]

        st.session_state.questions = questions
        st.session_state.index = 0

    # Show question
    if st.session_state.questions and st.session_state.index < len(st.session_state.questions):

        st.subheader(f"Question {st.session_state.index + 1}")
        st.write(st.session_state.questions[st.session_state.index])

        answer = st.text_area("Your Answer", key=f"ans_{st.session_state.index}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Next Question", key="next_q"):
                st.session_state.index += 1

        with col2:
            if st.button("Reset Interview", key="reset_q"):
                st.session_state.questions = []
                st.session_state.index = 0

    elif st.session_state.questions:
        st.success("🎉 Interview Completed!")
# =========================
# 📝 TAB 3 - RESUME BUILDER
# =========================
with tab3:
    st.header("📝 AI Resume Builder")

    name = st.text_input("Name", key="name")
    skills = st.text_area("Skills", key="skills")
    experience = st.text_area("Experience", key="experience")
    projects = st.text_area("Projects", key="projects")
    role_target = st.text_input("Target Job Role", key="role_target")

    if st.button("Generate Resume", key="resume_btn"):
        with st.spinner("Building Resume..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Create a professional ATS-friendly resume for:

Name: {name}
Skills: {skills}
Experience: {experience}
Projects: {projects}
Target Role: {role_target}

Also give improvement suggestions.
"""
                    }
                ]
            )

        st.success("Resume Generated ✅")
        st.write(response.choices[0].message.content)
    if st.button("Download Resume PDF"):

     from io import BytesIO
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    resume_text = st.session_state.get("resume_text", "No resume found")

    c.drawString(100, 750, "AI Generated Resume")
    c.drawString(100, 730, resume_text[:2000])  # safe limit

    c.save()
    buffer.seek(0)

    st.download_button(
        label="Download PDF",
        data=buffer,
        file_name="resume.pdf",
        mime="application/pdf"
    )

# =========================
# 📊 TAB 4 - ANALYZER
# =========================
with tab4:
    st.header("📊 Resume Analyzer")

    uploaded_file = st.file_uploader("📄 Upload Your Resume", type=["pdf", "docx", "txt"])

    resume_text = ""

    if uploaded_file is not None:

        # PDF handling
        if uploaded_file.type == "application/pdf":
            import PyPDF2

            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text()

        # DOCX handling
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            import docx

            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                resume_text += para.text + "\n"

        # TXT handling
        else:
            resume_text = uploaded_file.read().decode("utf-8")

        st.success("Resume Uploaded Successfully ✅")

        st.text_area("Extracted Resume Text", resume_text, height=200)

    if st.button("Analyze Resume"):

        if resume_text.strip() == "":
            st.warning("Please upload a resume first")
        else:
            st.write("🔍 Analysis Result:")
            st.write("✔ Strength: Good technical skills")
            st.write("❌ Weakness: Add more projects")
            st.write("📌 Suggestion: Improve DSA and System Design")
# =========================
# 📚 TAB 5 - STUDY PLAN
# =========================
with tab5:
    st.header("Skill Gap Analysis + Study Plan")

    resume_text = st.text_area("Paste Resume", key="resume2")
    target_role = st.text_input("Target Role", key="role_s")

    if st.button("Generate Study Plan"):
        response = requests.post(
            f"{BASE_URL}/study-plan",
            json={
                "resume": resume_text,
                "role": target_role
            }
        )

        st.write(response.json()["plan"])

# =========================
# 📈 TAB 6 - ANALYTICS (SIMPLE UI)
# =========================
with tab6:
    st.header("Performance Analytics")

    st.metric("Average Score", "7.8")
    st.metric("Interviews", "5")
    st.metric("Best Score", "9")

    st.line_chart([6, 7, 8, 7, 9])
    st.markdown("""
---
<div style="text-align:center; color:#94a3b8; padding:20px; font-size:13px;">

🚀 AI Interview Prep Platform  
Helping students crack interviews with AI-powered tools

<br>

📧 support@aiinterviewprep.com | 📞 +91-XXXXXXXXXX

<br><br>

© 2026 AI Interview Prep. All Rights Reserved.

<br>

<span style="color:#60a5fa;">
Built with ❤️ using Streamlit & AI
</span>

</div>
""", unsafe_allow_html=True)

st.markdown("""
---
<div style="display:flex; justify-content:space-between; color:#94a3b8; font-size:12px; padding:20px;">

<div>
<b style="color:white;">AI Interview Prep</b><br>
Smart AI Career Assistant
</div>

<div>
📧 support@aiinterviewprep.com<br>
📞 +91-XXXXXXXXXX
</div>

<div>
© 2026 All Rights Reserved<br>
Built for Students 🚀
</div>

</div>
""", unsafe_allow_html=True)