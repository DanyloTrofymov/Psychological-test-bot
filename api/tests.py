import os
import requests
from app_types.paginatedResponse import PaginatedResponse
from app_types.quiz import QuizResponse

API_URL = os.getenv("API_URL")


def fetch_tests(params: dict = None) -> PaginatedResponse[QuizResponse]:
    """
    Fetch tests from the backend API.

    :param endpoint: The API endpoint to fetch data from.
    :param params: Optional query parameters for the request.
    :return: The response data as a dictionary.
    """
    response = requests.get(f"{API_URL}/quiz", params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def fetch_tests_by_id(id: str, token: str) -> dict:
    """
    Fetch test by id from the backend API.

    :param endpoint: The API endpoint to fetch data from.
    :param params: Optional query parameters for the request.
    :return: The response data as a dictionary.
    """
    response = requests.get(f"{API_URL}/quiz/{id}", headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status() 
    return response.json()
