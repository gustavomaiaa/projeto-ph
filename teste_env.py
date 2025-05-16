# teste_env.py
from dotenv import load_dotenv
import os

load_dotenv()
print("DATABASE_URI:", os.getenv("DATABASE_URI"))
