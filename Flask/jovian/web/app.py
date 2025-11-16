from flask import Flask, render_template, jsonify
from database import load_jobs_from_db, load_job_from_db

app = Flask(__name__)

# -----------------------------
# Home page: list all jobs
# -----------------------------
@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()  # returns list of dicts
    return render_template("home.html", jobs=jobs)

# -----------------------------
# API endpoint: all jobs
# -----------------------------
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()  # list of dicts
    return jsonify(jobs)

# -----------------------------
# API endpoint: single job by ID
# -----------------------------
@app.route("/api/job/<int:id>")
@app.route("/api/jobs/<int:id>")
def api_show_job(id):
    job = load_job_from_db(id)
    if job is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

# -----------------------------
# Job Page: single job
# -----------------------------
@app.route("/job/<int:id>")
@app.route("/jobs/<int:id>")
def web_show_job(id):
    job = load_job_from_db(id)
    if job is None:
        return {"error": "Job not found"}, 404
    return render_template('job.html', job=job)

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
