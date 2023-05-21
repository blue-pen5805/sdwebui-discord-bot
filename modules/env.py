import os
from dotenv import load_dotenv

load_dotenv()

def get(key: str):
    return os.environ.get(key)
