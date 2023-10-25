import os
import threading
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from keep_alive import keep_alive_ping, keep_alive
from tg import start, handle_txt, handle_voice

keep_alive_ping()

# Define the Telegram bot token from the environment variable
bot_token = os.environ['BOT_TOKEN']

def main():
    # Create an instance of the Updater class using the bot token
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    
    # Register the start command    
    dp.add_handler(CommandHandler("start", start))
    # handler to capture voice messages
    dp.add_handler(MessageHandler(Filters.voice & ~Filters.text, handle_voice))
    # handler to capture text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_txt))

    # Start the bot
    updater.start_polling()

    # Create a separate thread for executing keep_alive
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()


    updater.idle()
    updater.stop()

if __name__ == '__main__':
    main()