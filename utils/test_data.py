import os
from dotenv import load_dotenv

load_dotenv()

# ─── Environment ─────────────────────────────────────────────────────────────
BASE_URL    = os.getenv("BASE_URL")
QA_EMAIL    = os.getenv("QA_EMAIL")
QA_PASSWORD = os.getenv("QA_PASSWORD")

# ─── Fixed per task spec ─────────────────────────────────────────────────────
ADDRESS         = "Sofia, Bulgaria"
PARTNER_TYPE    = "Service"
LOGO_PATH       = os.path.join(
    os.path.dirname(__file__), "..", "fixtures", "test_logo.png"
)

# ─── Fixed contact details ────────────────────────────────────────────────────
# Used as stable phone number across all test runs
PHONE           = "+359123456789"