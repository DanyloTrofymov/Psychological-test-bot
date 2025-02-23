import os
import requests
from typing import List

from app_types.helpingCenter import HelpingCenterResponse
from dotenv import load_dotenv
load_dotenv()
API_URL = os.getenv("API_URL")

def fetch_centers() -> List[HelpingCenterResponse]:
    response = requests.get(f"{API_URL}/helping-centers")
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()
