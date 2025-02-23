import time

from telegram import Update
from telegram.ext import ContextTypes
from jwt import decode, ExpiredSignatureError, InvalidTokenError
import api.auth as auth


async def authorization_helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    isValid = False 
    if 'auth' in context.user_data:
        token = context.user_data['auth']
        try:
            decoded_token = decode(token, options={"verify_signature": False})
            if 'exp' in decoded_token and decoded_token['exp'] >= time.time():
              isValid = True
        except ExpiredSignatureError:
            print(f"Token has expired {update.effective_user.username} ({update.effective_user.id})")
        except InvalidTokenError:
            print(f"Invalid token {update.effective_user.username} ({update.effective_user.id})")
    else:
        print(f"No auth token found in user_data for {update.effective_user.username} ({update.effective_user.id})")
    
    if not isValid:
      await auth.sign_in(update, context)
