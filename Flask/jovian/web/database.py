import os
from sqlalchemy import create_engine, MetaData, Table, select

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

# SSL certificate from env variable
SSL_CA_CONTENT = os.getenv("SSL_CA_CONTENT")
if not SSL_CA_CONTENT:
    raise ValueError("Environment variable SSL_CA_CONTENT is not set!")

# Write the PEM to a temporary file
ssl_ca_path = "/tmp/ca.pem"
with open(ssl_ca_path, "w") as f:
    f.write(SSL_CA_CONTENT)

# -----------------------------
# 2️⃣ Create engine securely with SSL
# -----------------------------
engine = create_engine(
    f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}",
    connect_args={"ssl_ca": ssl_ca_path},
    echo=True
)

# -----------------------------
# 3️⃣ Reflect the existing jobs table
# -----------------------------
metadata = MetaData()
metadata.reflect(bind=engine)

# Debug: print available tables
print("Available tables:", list(metadata.tables.keys()))

jobs_table = metadata.tables.get("jobs")
if jobs_table is None:
    raise ValueError("Table 'jobs' does not exist in the database!")

# -----------------------------
# 4️⃣ Query all jobs
# -----------------------------
stmt = select(jobs_table)

def load_jobs_from_db():
    with engine.connect() as conn:
        results = conn.execute(stmt).mappings().all()  # returns list of dicts
    return results

if __name__ == "__main__":
    results = load_jobs_from_db()
    for row in results:
        print(row)
