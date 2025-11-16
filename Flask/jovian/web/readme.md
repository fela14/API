🏢 Hale Careers Website

A job listing and application portal built with Flask and MySQL, designed to showcase opportunities and allow applicants to submit their information securely.

🔗 Live Site: https://hale-careers-website.onrender.com/

📅 Hosted on Render from Nov 16, 2025 for the next few days.

✨ Features

📄 Browse all available jobs with detailed descriptions

📝 Apply to jobs via a web form capturing:

👤 Full Name

📧 Email

🔗 LinkedIn URL

🎓 Education

💼 Work Experience

📄 Resume URL

🛡️ hCaptcha integration: Prevents spam by requiring verification before submission

📬 Mailjet integration: Sends a confirmation email to applicants upon successful submission

🖥️ Admin panel: View all applications or filter by specific job


🛠️ Tech Stack

Backend: Flask

Database: MySQL (with SSL)

ORM: SQLAlchemy

Email Service: Mailjet

Captcha: hCaptcha

⚙️ Setup Instructions

Clone the repository:

git clone <repo_url>
cd hale-careers-website


Install dependencies:

pip install -r requirements.txt


Set environment variables:

export HCAPTCHA_SECRET="your-hcaptcha-secret"
export MJ_API_KEY="your-mailjet-api-key"
export MJ_API_SECRET="your-mailjet-secret"
export MJ_SENDER_EMAIL="noreply@yourdomain.com"
export PASSWORD="your-database-password"
export SSL_CA_CONTENT="your-ssl-ca-content"


Run the application:

python app.py or flask run

📝 How It Works

Users browse jobs on the home page 🏠

Clicking “Apply” opens the application form 📝

Users complete hCaptcha verification 🛡️ before submission

Submitted data is stored securely in the database 💾

Applicants receive a confirmation email 📬 