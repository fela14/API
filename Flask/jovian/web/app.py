from flask import Flask, render_template, request, jsonify
from database import (
    load_jobs_from_db,
    load_job_from_db,
    add_application_to_db,
    load_all_applications,
    load_applications_for_job
)
import requests
from mailjet_rest import Client
import os

# hCaptcha secret key
HCAPTCHA_SECRET = os.getenv("HCAPTCHA_SECRET")

# Mailjet credentials
MJ_API_KEY = os.getenv("MJ_API_KEY")
MJ_API_SECRET = os.getenv("MJ_API_SECRET")
MJ_SENDER_EMAIL = os.getenv("MJ_SENDER_EMAIL")  # e.g., "noreply@yourdomain.com"
MJ_SENDER_NAME = "Hale Careers"

app = Flask(__name__)

# -----------------------------
# Home page: list all jobs
# -----------------------------
@app.route("/")
def home():
    jobs = load_jobs_from_db()
    return render_template("home.html", jobs=jobs)

# -----------------------------
# API: all jobs
# -----------------------------
@app.route("/api/jobs")
def api_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)

# -----------------------------
# API: single job
# -----------------------------
@app.route("/api/job/<int:id>")
@app.route("/api/jobs/<int:id>")
def api_job(id):
    job = load_job_from_db(id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

# -----------------------------
# Web: job page
# -----------------------------
@app.route("/job/<int:id>")
@app.route("/jobs/<int:id>")
def job_page(id):
    job = load_job_from_db(id)
    if job is None:
        return {"error": "Job not found"}, 404
    return render_template("job.html", job=job)

# -----------------------------
# Apply to a job
# -----------------------------
@app.route("/job/<int:id>/apply", methods=['POST'])
def apply_to_job(id):
    data = request.form.to_dict()
    job = load_job_from_db(id)

    # -----------------------------
    # 1️⃣ Verify hCaptcha
    # -----------------------------
    hcaptcha_response = data.get("h-captcha-response")
    if not hcaptcha_response:
        return "hCaptcha verification failed. Please try again.", 400

    verify_url = "https://hcaptcha.com/siteverify"
    payload = {
        "secret": HCAPTCHA_SECRET,
        "response": hcaptcha_response
    }
    resp = requests.post(verify_url, data=payload).json()
    if not resp.get("success"):
        return "hCaptcha verification failed. Please try again.", 400

    # -----------------------------
    # 2️⃣ Save application to DB
    # -----------------------------
    add_application_to_db(id, data)
    data['job_id'] = id

    # -----------------------------
    # 3️⃣ Send confirmation email via Mailjet
    # -----------------------------
    mailjet = Client(auth=(MJ_API_KEY, MJ_API_SECRET), version='v3.1')
    message = {
        'Messages': [
            {
                "From": {"Email": MJ_SENDER_EMAIL, "Name": MJ_SENDER_NAME},
                "To": [{"Email": data.get("email"), "Name": data.get("full_name")}],
                "Subject": f"Application Received for {job['title']}",
                "TextPart": f"Hi {data.get('full_name')},\n\nThank you for applying to {job['title']}.\nWe will review your application and get back to you soon.",
                "HTMLPart": f"<h3>Hi {data.get('full_name')},</h3><p>Thank you for applying to <b>{job['title']}</b>.</p><p>We will review your application and get back to you soon.</p>"
            }
        ]
    }
    mailjet.send.create(data=message)

    # -----------------------------
    # 4️⃣ Render submitted page
    # -----------------------------
    return render_template("submitted.html", application=data, job=job)

# -----------------------------
# Admin: view ALL applications
# -----------------------------
@app.route("/admin/applications")
def admin_all_applications():
    applications = load_all_applications()
    return render_template("admin_applications.html", applications=applications)

# -----------------------------
# View applications for ONE job
# -----------------------------
@app.route("/job/<int:id>/applications")
def job_applications(id):
    job = load_job_from_db(id)
    applications = load_applications_for_job(id)
    return render_template("job_applications.html", job=job, applications=applications)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
