import os
from sqlalchemy import create_engine, MetaData, Table, select, text

# -----------------------------
# 1️⃣ Connection parameters
# -----------------------------
USER = "avnadmin"
HOST = "jovian-careers-mysql-fela14.i.aivencloud.com"
PORT = 10013
DB = "halecareers"

# Get password from environment variable
PASSWORD = os.getenv("PASSWORD")
if not PASSWORD:
    raise ValueError("Environment variable PASSWORD is not set!")

# SSL certificate from environment variable
SSL_CA_CONTENT = os.getenv("SSL_CA_CONTENT")
if not SSL_CA_CONTENT:
    raise ValueError("Environment variable SSL_CA_CONTENT is not set!")

# Write the SSL CA certificate to a temporary file
ssl_ca_path = "/tmp/ca.pem"
with open(ssl_ca_path, "w") as f:
    f.write(SSL_CA_CONTENT)

# -----------------------------
# 2️⃣ Create SQLAlchemy engine securely with SSL
# -----------------------------
engine = create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
    connect_args={"ssl_ca": ssl_ca_path},
    echo=True
)

# -----------------------------
# 3️⃣ Reflect the existing tables
# -----------------------------
metadata = MetaData()
metadata.reflect(bind=engine)

# Debug: print available tables
print("Available tables:", list(metadata.tables.keys()))

# Access the jobs table
jobs_table = metadata.tables.get("jobs")
if jobs_table is None:
    raise ValueError("Table 'jobs' does not exist in the database!")

# -----------------------------
# 4️⃣ Define statements for queries
# -----------------------------
stmt_all_jobs = select(jobs_table)

# -----------------------------
# 5️⃣ Functions to load jobs
# -----------------------------
def load_jobs_from_db():
    """Return all jobs as a list of dictionaries"""
    with engine.connect() as conn:
        results = conn.execute(stmt_all_jobs).mappings().all()
    return results

def load_job_from_db(job_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :val"),
            {"val": job_id}
        ).mappings().fetchone()  # <--- use .mappings() here
        if result is None:
            return None
        return dict(result)  # now this works

# -----------------------------
# 6️⃣ Optional: test when run standalone
# -----------------------------
if __name__ == "__main__":
    all_jobs = load_jobs_from_db()
    print(f"Total jobs found: {len(all_jobs)}")
    for job in all_jobs:
        print(job)

    # Example: load job with id=1
    single_job = load_job_from_db(1)
    print("\nJob with ID 1:")
    print(single_job)
