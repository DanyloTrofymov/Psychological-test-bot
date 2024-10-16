import os
import requests

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

