import os
import requests
from typing import List

from app_types.commonProblems import CommonProblemsResponse
API_URL = os.getenv("API_URL")

def fetch_problems() -> List[CommonProblemsResponse]:
    response = requests.get(f"{API_URL}/common-problems")
    response.raise_for_status() 
    return response.json()


def fetch_problem_by_id(id: str) -> CommonProblemsResponse:
    response = requests.get(f"{API_URL}/common-problems/{id}")
    response.raise_for_status() 
    return response.json()
