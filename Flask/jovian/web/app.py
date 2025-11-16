from flask import Flask, render_template, request, jsonify
from database import (
    load_jobs_from_db,
    load_job_from_db,
    add_application_to_db,
    load_all_applications,
    load_applications_for_job
)

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

    add_application_to_db(id, data)

    data['job_id'] = id

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
