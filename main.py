from dotenv import load_dotenv
import os, sys, subprocess, logging, psutil, time
import telebot
from telebot import types

# Enable logging
logging.basicConfig(filename='bot_activity.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Function to convert seconds into human-readable format
def seconds_to_human_readable(seconds):
    seconds = int(seconds)
    weeks = seconds // (7 * 24 * 3600)
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if weeks > 0:
        return f"{weeks}W {days}D, {hours}hr"
    elif days > 0:
        return f"{days}D {hours}hr"
    elif hours > 0:
        return f"{hours}hr {minutes}min"
    else:
        return f"{minutes}min {seconds}sec"

# Function to get the system uptime
def get_human_readable_system_uptime():
    boot_time_timestamp = psutil.boot_time()
    current_time_timestamp = time.time()
    uptime_seconds = current_time_timestamp - boot_time_timestamp
    return seconds_to_human_readable(uptime_seconds)

# Check if any arguments are provided
# (useful for finding the right python.exe instance in task manager's "command" column)
if len(sys.argv) > 1:
    arg = sys.argv[1]
    logging.info(f'Script "batter-bot" started with argument: {arg}')
else:
    logging.info('Script "batter-bot" started without arguments')

# Environment Variables
load_dotenv() # Load environment variables from .env file
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_ID = int(os.getenv('TELEGRAM_ALLOWED_ID'))
PC_NAME = os.getenv('PC_NAME')

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def list_bat_files():
    # Exclude 'run_script.bat' from the list
    return [f for f in os.listdir('./bats') if f.endswith('.bat') and f != 'run_script.bat']

#####################
# Handler Functions #
#####################
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ALLOWED_ID:
        bot.send_message(message.chat.id, "👋🤖")
        logging.info(f'Bot started by user {message.chat.id}')
    else:
        logging.warning(f"⚠️ Unauthorized start attempt by user {message.chat.id}")
        bot.send_message(ALLOWED_ID, f"⚠️ Unauthorized start attempt by user {message.chat.id}")

@bot.message_handler(commands=['status','check','running','update'])
def send_status(message):
    if message.chat.id == ALLOWED_ID:
        status_message = f"⚙️ Still running on `{PC_NAME}`.\n⌛ System uptime: {get_human_readable_system_uptime()}"
        bot.send_message(message.chat.id, status_message, parse_mode='Markdown')
        logging.info(f'Bot sent status to user {message.chat.id}')
        logging.info(f'Status message: {status_message}')
    else:
        logging.warning(f"⚠️ Unauthorized status request by user {message.chat.id}")
        bot.send_message(ALLOWED_ID, f"⚠️ Unauthorized status request by user {message.chat.id}")

""" # No need to expose this publicly now that I already know my chat id
@bot.message_handler(commands=['chatid'])
def send_chat_id(message):
    bot.send_message(message.chat.id, f"🤖 Your Chat ID is: `{message.chat.id}`", parse_mode='Markdown')
    logging.info(f'Chat ID requested by user {message.chat.id}')
"""

@bot.message_handler(commands=['runbat','bat','bats'])
def send_bat_files(message):
    if message.chat.id == ALLOWED_ID:
        bat_files = list_bat_files()
        if not bat_files:
            bot.send_message(message.chat.id, "No `.bat` files found.", parse_mode='Markdown')
            logging.info(f'No .bat files found by user {message.chat.id}')
            return
    
        markup = types.InlineKeyboardMarkup()
        for file in bat_files:
            markup.add(types.InlineKeyboardButton(file, callback_data=file))
        bot.send_message(message.chat.id, "🖥️ Tap a `.bat` file to run it:", reply_markup=markup, parse_mode='Markdown')
        logging.info(f'.bat files list sent to user {message.chat.id}')
    else:
        logging.warning(f"⚠️ Unauthorized .bat list attempt by user {message.chat.id}")
        bot.send_message(ALLOWED_ID, f"⚠️ Unauthorized `.bat` list attempt by user {message.chat.id}", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_file_selection(call):
    if call.message.chat.id == ALLOWED_ID:
        bat_file = call.data
        if bat_file in list_bat_files():
            try:
                bat_file = f".\\bats\\{bat_file}"
                subprocess.run(bat_file, shell=True, check=True)
                bot.answer_callback_query(call.id, f"`{bat_file}` executed successfully!")
                logging.info(f'{bat_file} executed by user {call.from_user.id}')
            except subprocess.CalledProcessError as e:
                bot.answer_callback_query(call.id, f"Failed to execute `{bat_file}`: {e}")
                logging.error(f"Failed to execute {bat_file}: {e}")
        else:
            bot.answer_callback_query(call.id, "File not found.")
            logging.error(f"File {bat_file} not found.")
    else:
        logging.warning(f"⚠️ Unauthorized .bat execution attempt by user {call.from_user.id}")
        bot.send_message(ALLOWED_ID, f"⚠️ Unauthorized `.bat` execution attempt by user {call.from_user.id}", parse_mode='Markdown')

#########################
# Main bot polling loop #
#########################
if __name__ == "__main__":
    # Send start message to the user
    #bot.send_message(ALLOWED_ID, "I am alive! 👋🤖")
    startup_message = f"👋 I just started up on `{PC_NAME}`.\n⌛ System uptime: {get_human_readable_system_uptime()}"
    bot.send_message(ALLOWED_ID, startup_message, parse_mode='Markdown')
    logging.info(f"Bot started and startup message sent to user {ALLOWED_ID}")
    logging.info(f"Startup message: {startup_message}")
    # Start bot loop
    bot.infinity_polling()
