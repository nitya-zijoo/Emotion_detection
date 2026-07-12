import requests
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
BASE_URL = f"https://identitytoolkit.googleapis.com/v1/accounts"

def register_user(email: str, password: str) -> dict:
    url = f"{BASE_URL}:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

def login_user(email: str, password: str) -> dict:
    url = f"{BASE_URL}:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    return response.json()

def send_verification_email(id_token: str) -> dict:
    url = f"{BASE_URL}:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {"requestType": "VERIFY_EMAIL", "idToken": id_token}
    response = requests.post(url, json=payload)
    return response.json()

def get_user_info(id_token: str) -> dict:
    url = f"{BASE_URL}:lookup?key={FIREBASE_API_KEY}"
    payload = {"idToken": id_token}
    response = requests.post(url, json=payload)
    data = response.json()
    if "users" in data:
        return data["users"][0]
    return data