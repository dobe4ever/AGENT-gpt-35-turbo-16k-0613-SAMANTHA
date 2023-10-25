import os
import subprocess
from telegram import Bot, ChatAction
from gpt import chatgpt, transcribe_voice
from speech import elevenlabs_gen

# Define the Telegram bot token from the environment variable
bot_token = os.environ['BOT_TOKEN']
user_id = os.environ['USER_ID']
troy_id = os.environ['TROY_ID']
bot = Bot(token=bot_token)

# start command
def start(update, context):
    response = open(os.path.abspath("downloads/start-response.mp3"), "rb")
    user_id = update.message.from_user.id
    bot_send_audio(user_id, response)

# Running the conversation
def handle_txt(update, context):
    # Get the user's info
    user_message = update.message.text
    user_id = update.message.from_user.id
    # Check if the message was sent from the specified user ID
    if user_id == int(user_id) or user_id == int(troy_id):
        # send message to gpt & get a response
        response = chatgpt(user_id, user_message)
        # generate audio response
        audio_response = elevenlabs_gen(response)
        # send audio response to the user
        bot_send_audio(user_id, audio_response)
        
        # send the "kill 1" command to reset container
        subprocess.run(["kill", "1"])

def handle_voice(update, context):
    # Check if the message was sent from the specified user ID
    user_id = update.message.from_user.id
    # Check if the message was sent from the specified user ID
    if user_id == int(user_id) or user_id == int(troy_id):
        # get voice
        file_id = update.message.voice.file_id
        file = bot.get_file(file_id)
        # Get file extension from the file_path
        extension = file.file_path.split('.')[-1]
        # download file
        file.download(f"downloads/voice-message.{extension}")
        # Open voice
        voice = open(os.path.abspath(
            f"downloads/voice-message.{extension}"), "rb")
        # transcribe voice
        transcript = transcribe_voice(voice)
        # Send transcript to GPT & get response
        response = chatgpt(user_id, transcript)
        # generate audio response
        audio_response = elevenlabs_gen(response)
        # send audio response to the user
        bot_send_audio(user_id, audio_response)

        # send the "kill 1" command to reset container
        subprocess.run(["kill", "1"])

def bot_send_text(user_id, text):
    bot.sendChatAction(chat_id=user_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")

def bot_send_audio(user_id, audio):
    bot.sendChatAction(chat_id=user_id, action=ChatAction.RECORD_AUDIO)
    bot.send_document(chat_id=user_id, document=audio)