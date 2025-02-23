import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_URL = os.getenv("API_URL")

def create_take(requestBody: dict, token: str):
    try:
        response = requests.post(
            f"{API_URL}/take",
            json=requestBody,      
            headers={"Authorization": f"Bearer {token}"}
        )
        return response
    except requests.exceptions.RequestException as e:
        print(e)

def fetch_latest_take_by_quiz_id(id: str, token: str):
    response = requests.get(f"{API_URL}/take/quiz/{id}/latest", headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status() 
    return response.json()