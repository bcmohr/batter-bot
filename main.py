from dotenv import load_dotenv
import os, logging
import telebot

# Enable logging
logging.basicConfig(filename='bot_activity.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Environment Variables
load_dotenv() # Load environment variables from .env file
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_ID = os.getenv('TELEGRAM_ALLOWED_ID')

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Handler functions
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ALLOWED_ID:
        bot.reply_to(message, "Hi there! 👋🤖")
        logging.info(f'Bot started by user {message.chat.id}')

@bot.message_handler(commands=['chatid'])
def send_chat_id(message):
    chat_id = message.chat.id
    response_message = f"🤖 Your Chat ID is: {chat_id}"
    bot.reply_to(message, response_message)
    logging.info(f'Chat ID requested by user {chat_id}')

#########################
# Main bot polling loop #
#########################
if __name__ == "__main__":
    # Send start message to the user
    bot.send_message(ALLOWED_ID, "I am alive! 👋🤖")
    # Start bot loop
    bot.infinity_polling()
