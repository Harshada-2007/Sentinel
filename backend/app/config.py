import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# If no Supabase credentials are configured, the app falls back to reading
# the local CSVs generated in backend/data/ so the demo runs fully offline.
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "ml", "saved_models")
