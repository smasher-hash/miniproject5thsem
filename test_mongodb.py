import os
import importlib.util

try:
    load_dotenv = importlib.import_module("dotenv").load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

try:
    MongoClient = importlib.import_module("pymongo").MongoClient
except ImportError:
    raise SystemExit("PyMongo is not installed. Install it with: python -m pip install pymongo")

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)
finally:
    client.close()