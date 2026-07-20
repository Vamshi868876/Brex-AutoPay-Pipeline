import os
from dotenv import load_dotenv

load_dotenv()

# Safety Settings
TEST_MODE = True # Set to False when you want real money to leave your account!

# Brex Constants
BREX_BASE_URL = "https://platform.brexapis.com"
BREX_USER_TOKEN = os.getenv("BREX_USER_TOKEN")

# Email Constants
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# AI Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
