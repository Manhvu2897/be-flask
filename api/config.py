import hashlib
import time
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

BASE_URL_API = "https://www.quantconnect.com/api/v2"

USER_ID = os.environ.get("QUANT_CONNECT_USER_ID")

PROJECT_ID = "15770834"

NODE_ID = "a71c40b5"

url: str = os.environ.get("SUPABASE_URL")

key: str = os.environ.get("SUPABASE_KEY")

jwt: str = os.environ.get("SUPABASE_JWT")

supabase: Client = create_client(url, key)

def generate_token(qc_api_token: str) -> str:
    time_stamped_token = qc_api_token + ':' + str(int(time.time()))
    # Get hased API token
    hashed_token = hashlib.sha256(time_stamped_token.encode('utf-8')).hexdigest()
    return hashed_token

def init_header() -> dict:
    headers = {
        'Timestamp': str(int(time.time()))
    }
    return headers