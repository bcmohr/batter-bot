from dotenv import load_dotenv
import os, subprocess, logging
import telebot
from telebot import types

# Enable logging
logging.basicConfig(filename='bot_activity.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Environment Variables
load_dotenv() # Load environment variables from .env file
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_ID = os.getenv('TELEGRAM_ALLOWED_ID')

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Define additional functions
def list_bat_files():
    return [f for f in os.listdir('.') if f.endswith('.bat')]

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

@bot.message_handler(commands=['runbat'])
def send_bat_files(message):
    bat_files = list_bat_files()
    if not bat_files:
        bot.send_message(message.chat.id, "No .bat files found.")
        return
    
    markup = types.InlineKeyboardMarkup()
    for file in bat_files:
        markup.add(types.InlineKeyboardButton(file, callback_data=file))
    bot.send_message(message.chat.id, "Choose a .bat file to run:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_file_selection(call):
    bat_file = call.data
    if bat_file in list_bat_files():
        try:
            subprocess.run(bat_file, shell=True, check=True)
            bot.answer_callback_query(call.id, f"{bat_file} executed successfully!")
        except subprocess.CalledProcessError as e:
            bot.answer_callback_query(call.id, f"Failed to execute {bat_file}: {e}")
    else:
        bot.answer_callback_query(call.id, "File not found.")

#########################
# Main bot polling loop #
#########################
if __name__ == "__main__":
    # Send start message to the user
    bot.send_message(ALLOWED_ID, "I am alive! 👋🤖")
    # Start bot loop
    bot.infinity_polling()
