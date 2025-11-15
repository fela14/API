from flask import Flask, render_template, jsonify
from database import load_jobs_from_db
from sqlalchemy import select

app = Flask(__name__)

JOBS = [
    {
        'id': 1,
        'title': 'Data Scientist',
        'location': 'Lagos, Nigeria',
        'salary': '$80,000'
    },
    {
        'id': 2,
        'title': 'Frontend Engineer',
        'location': 'Soweto, South Africa',
        'salary': '$100,000'
    },
    {
        'id': 3,
        'title': 'Backend Engineer',
        'location': 'Remote',
    },
    {
        'id': 4,
        'title': 'AI Engineer',
        'location': 'San Francisco, USA',
        'salary': '$120,000'
    }
]

@app.route("/")
def hello_world():
    JOBS_SQL = load_jobs_from_db()
    return render_template('home.html', jobs=JOBS_SQL)

@app.route("/api/jobs")
def list_jobs():
    JOBS_SQL = load_jobs_from_db()  # returns list of RowMapping
    # Convert RowMapping objects to plain dicts
    jobs_list = [dict(job) for job in JOBS_SQL]
    return jsonify(jobs_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
