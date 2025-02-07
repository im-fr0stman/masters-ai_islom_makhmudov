import os

# ✅ OpenAI API Key (Stored Securely in Environment Variable)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Set OPENAI_API_KEY environment variable.")

# ✅ Database Path
DATABASE_PATH = "db/countries_database.sqlite"

# ✅ Logging Configuration
LOG_FILE = "logs/app.log"

# ✅ External API Configuration (Example API for Business Insights)
EXTERNAL_API_URL = "https://api.example.com/data"

# ✅ Email Settings (For sending query results)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
