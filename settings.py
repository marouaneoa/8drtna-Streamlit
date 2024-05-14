import supabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

def init():
    global supabase_url
    supabase_url = SUPABASE_URL
    global supabase_key
    supabase_key = SUPABASE_API_KEY
    global supabase_client
    supabase_client = supabase.create_client(supabase_url, supabase_key)