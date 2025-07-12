import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
IMAGE_ANALYZER=os.getenv("IMAGE_ANALYZER")
# Application Settings
USERNAME = os.getenv('USERNAME', 'User')
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'Jarvis')
