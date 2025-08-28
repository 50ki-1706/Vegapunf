import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, verbose=True)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", None)
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", None)
