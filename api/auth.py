import os
import time
import hashlib
import requests
from telegram import Update
from telegram.ext import ContextTypes
import hashlib
import requests
import hmac
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def sign_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Fetch user profile photos (Optional)
    photo_url = None
    if user.is_bot is False:
        photos = await context.bot.get_user_profile_photos(user.id)
        if photos.total_count > 0:
            file = await context.bot.get_file(photos.photos[0][-1].file_id)
            photo_url = file.file_path  # This is a Telegram file URL

    # Prepare user data
    user_data = {
        'auth_date': int(time.time()),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'id': user.id,
        'photo_url': photo_url,
    }

    # Generate a secret key by hashing the BOT_TOKEN with SHA-256
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    # Generate a hash for data verification using HMAC with the secret key
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(user_data.items()) if v is not None])
    user_data['hash'] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Send data to your backend
    try:
        response = requests.post(f"{API_URL}/auth/signIn", json=user_data)
        response.raise_for_status()
        context.user_data['auth'] = response.json()['accessToken']
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error sending data to backend: {e}')

def refresh_token(refresh_token: str) -> dict:
    response = requests.get(f"{API_URL}/refreshToken", headers={"Authorization": f"Bearer {refresh_token}"})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()