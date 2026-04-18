from flask import Flask, request, jsonify, send_file
from groq import Groq
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)

client = Groq(api_key="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")  # put your key here

# =========================
# 📄 QUESTIONS API
# =========================
@app.route("/questions", methods=["POST"])
def questions():
    data = request.json
    role = data.get("role")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Give 5 interview questions with answers for {role}"
        }]
    )

    return jsonify({"questions": response.choices[0].message.content})


# =========================
# 🎤 MOCK INTERVIEW API
# =========================
@app.route("/mock-interview", methods=["POST"])
def mock_interview():
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": "Give 5 interview questions for a software developer in numbered format"
        }]
    )

    return jsonify({"questions": response.choices[0].message.content})


# =========================
# 📝 RESUME BUILDER API
# =========================
@app.route("/resume", methods=["POST"])
def resume():
    data = request.json

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Create ATS resume:

Name: {data['name']}
Skills: {data['skills']}
Experience: {data['experience']}
Projects: {data['projects']}
Role: {data['role']}
"""
        }]
    )

    return jsonify({"resume": response.choices[0].message.content})


# =========================
# 📊 RESUME ANALYZER API
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Analyze resume:

{data['resume']}

Give strengths, weaknesses, suggestions, missing skills
"""
        }]
    )

    return jsonify({"analysis": response.choices[0].message.content})


# =========================
# 📚 STUDY PLAN API
# =========================
@app.route("/study-plan", methods=["POST"])
def study_plan():
    data = request.json

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
Analyze resume and role:

Resume: {data['resume']}
Role: {data['role']}

Give:
- Skill gaps
- Weak areas
- 7 day plan
"""
        }]
    )

    return jsonify({"plan": response.choices[0].message.content})


# =========================
# 📄 PDF DOWNLOAD API
# =========================
@app.route("/download-resume", methods=["POST"])
def download_resume():
    data = request.json

    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.drawString(100, 750, "AI GENERATED RESUME")
    c.drawString(100, 730, data.get("content", "No Content"))
    c.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)