import os
import socketio
from telegram.constants import ParseMode
from utils.keyboards import Keyboards
from dotenv import load_dotenv
from datetime import datetime 
load_dotenv()
API_URL = os.getenv("API_URL")

disclaimer = '_Дана відповідь підготовлена за допомогою штучного інтелекту та не є професійною рекомендацією._\n\n'

class AIChatHandler:
    def __init__(self, context, message):
        self.context = context
        self.message = message
        self.sio = socketio.AsyncClient()
        self.chatroom_id = None
        self.last_edit = datetime.now()
        self.partial_response = disclaimer
        self.register_events()

    def register_events(self):
        @self.sio.event(namespace='/chat')
        async def connect():
            print("Connected to WebSocket server")

        @self.sio.event(namespace='/chat')
        async def connect_error(data):
            print("Connection failed:", data)

        @self.sio.event(namespace='/chat')
        async def disconnect():
            print("Disconnected from WebSocket server")

        @self.sio.on('chatroomDetails', namespace='/chat')
        async def on_chatroom_details(data):
            # Store the chatroom ID
            self.chatroom_id = data['id']
            print(f"Chatroom ID set: {self.chatroom_id}, {data}")

        @self.sio.on('aiPartMessage', namespace='/chat')
        async def on_ai_part_message(data):
            #print(f"Received aiPartMessage: {data}")
            print(f"Current chatroom ID: {self.chatroom_id}")
            if data['chatroomId'] == self.chatroom_id:
                partial_text = data['message']
                self.partial_response += partial_text
                print(f"Updating message with partial response: {self.partial_response}")
                try:
                  if (datetime.now() - self.last_edit).seconds > 3:
                    await self.context.bot.edit_message_text(
                        chat_id=self.message.chat_id,
                        message_id=self.message.message_id,
                        text=self.partial_response + '...',
                        parse_mode=ParseMode.MARKDOWN
                        )
                    print("Message updated successfully")
                    self.last_edit = datetime.now()
                except Exception as e:
                    print(f"Error editing message: {e}")

        @self.sio.on('aiEndMessage', namespace='/chat')
        async def on_ai_end_message(data):
            print(f"AI End Message: {data}")
            if data['chatroomId'] == self.chatroom_id:
                await self.context.bot.send_message(
                    chat_id=self.message.chat_id,
                    text=f"{disclaimer}{data['message']}",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=Keyboards.cancelKeyboard
                )
                await self.context.bot.delete_message(
                    chat_id=self.message.chat_id,
                    message_id=self.message.message_id
                )

    async def start(self, token):
        if not self.sio.connected:
            await self.sio.connect(f'{API_URL}', transports=['websocket', 'polling'], auth={'token': f'{token}'})
        await self.sio.emit('AICreateChatroom', {
        'disableRunResponse': True
        },
        namespace='/chat')

    async def send_message(self, message):
      self.partial_response = disclaimer
      await self.sio.emit('sendAiMessage', {
        'message': message,
        'chatroomId': self.chatroom_id
      }, namespace='/chat')

    async def finish(self):
        if self.sio.connected:
            await self.sio.disconnect()
