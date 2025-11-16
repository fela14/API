import os
from sqlalchemy import create_engine, MetaData, Table, select, text

# -----------------------------
# Database connection settings
# -----------------------------
USER = "avnadmin"
HOST = "jovian-careers-mysql-fela14.i.aivencloud.com"
PORT = 10013
DB = "halecareers"

PASSWORD = os.getenv("PASSWORD")
if not PASSWORD:
    raise ValueError("Environment variable PASSWORD is not set!")

SSL_CA_CONTENT = os.getenv("SSL_CA_CONTENT")
if not SSL_CA_CONTENT:
    raise ValueError("Environment variable SSL_CA_CONTENT is not set!")

ssl_ca_path = "/tmp/ca.pem"
with open(ssl_ca_path, "w") as f:
    f.write(SSL_CA_CONTENT)

# -----------------------------
# Create SQLAlchemy engine (SSL)
# -----------------------------
engine = create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
    connect_args={"ssl_ca": ssl_ca_path},
    echo=True
)

# -----------------------------
# Reflect tables
# -----------------------------
metadata = MetaData()
metadata.reflect(bind=engine)

print("Available tables:", list(metadata.tables.keys()))

jobs_table = metadata.tables.get("jobs")
if jobs_table is None:
    raise ValueError("Table 'jobs' does not exist!")

# -----------------------------
# Load all jobs
# -----------------------------
stmt_all_jobs = select(jobs_table)

def load_jobs_from_db():
    """Return all jobs as a list of dictionaries"""
    with engine.connect() as conn:
        results = conn.execute(stmt_all_jobs).mappings().all()  # RowMapping objects
        # Convert to list of dicts
        return [dict(row) for row in results]

# -----------------------------
# Load one job
# -----------------------------
def load_job_from_db(job_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :val"),
            {"val": job_id}
        ).mappings().fetchone()

        if result is None:
            return None

        return dict(result)

# -----------------------------
# Add application
# -----------------------------
def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("""
            INSERT INTO applications 
            (job_id, full_name, email, linkedin_url, education, work_experience, resume_url)
            VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
        """)

        conn.execute(
            query,
            {
                "job_id": job_id,
                "full_name": data.get("full_name"),
                "email": data.get("email"),
                "linkedin_url": data.get("linkedin"),
                "education": data.get("education"),
                "work_experience": data.get("work_experience"),
                "resume_url": data.get("resume"),
            }
        )

        conn.commit()

# -----------------------------
# Load ALL applications
# -----------------------------
def load_all_applications():
    with engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM applications")
        ).mappings().all()

# -----------------------------
# Load applications for ONE job
# -----------------------------
def load_applications_for_job(job_id):
    with engine.connect() as conn:
        return conn.execute(
            text("SELECT * FROM applications WHERE job_id = :jid"),
            {"jid": job_id}
        ).mappings().all()

# -----------------------------
# Debug runner
# -----------------------------
if __name__ == "__main__":
    print(load_jobs_from_db())
