# Telegram Display Configuration Bot (Batter Bot)

This Python-based Telegram bot facilitates remote management of PC display configurations through the execution of specific .bat files located in the same directory as the script. It is designed to offer a convenient interface for users to change their display settings via Telegram commands. Originally named Batter Bot after the intended purpose of running `.bat` files. Thus, `.bat`ter Bot!

## Features

- Logging: Comprehensive logging of bot activities, including command usage and execution outcomes, to a file named `bot_activity.log`.
- Environment Variable Management: Utilizes `.env` for secure storage and retrieval of essential configurations like Telegram bot token and allowed user ID.
- Command Handling: Supports several commands for user interaction:
  - `/start` - The bot just waves to you. Which is neat.
  - `/runbat` - Lists available .bat files for display configuration and executes them upon user selection.
  - `/status` - Shows the PC name and the uptime of the host machine.
- Secure Execution of .bat Files: Executes selected `.bat` files safely, handling successes and failures gracefully.
- Alerts for Unauthorized Attempts: Alerts the specified user of attempts to use the bot originating from other users.

## Setup
### Prerequisites

- Python 3.x
- `python-telegram-bot` library
- `python-dotenv library` for environment variable management

### Installation

1. Clone the repository to your local machine.
2. (*Optional*) Create and then activate a python virtual environment

```
python -m venv venv
.\.venv\Scripts\activate
```

3. Install the required packages:

- **Option 1**: From `requirements.txt`
```
pip install -r requirements.txt
```

- **Option 2**: Manually install core packages and pray
```
pip install python-telegram-bot python-dotenv psutil
```

4. Create a `.env` file in the root directory of the project with the following variables:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ALLOWED_ID=your_telegram_user_id_here
PC_NAME=name_of_the_system_running_the_bot_here
```

5. Replace `your_bot_token_here` and `your_telegram_user_id_here` with your actual Telegram bot token and Telegram user ID, respectively.
6. Replace `name_of_the_system_running_the_bot_here` with an identifier for the system running this bot.

### Usage

Note: Ensure the `.bat` files you want to use are in the `bats` directory. These `.bat` files should be named in a way that describes their function. For example, `TvOnly_4k.bat`, `Default_3x_1440p.bat`, and `CenterOnly_1440p.bat` are files that may apply various display settings.

- **Option 1**: Start the bot as a nicely hidden Windows background process by running the included `start_batter_bot_hidden.vbs` script. Once running, the bot's python script can be found in task manager as `python.exe` with `batter-bot_startup` in the `command line` column. You may need to add this column to task manager, I don't think it is visible by default. Just right click any column header in task manager to see what columns you can make visible.

- **Option 2**: Start the bot in its own window by running the `start_batter_bot.bat` script.

- **Option 3**: Start the bot manually by running:

```
.\.venv\Scripts\activate
python telegram_display_bot.py
```

## Security

This bot is configured to respond only to commands from a specified Telegram user ID, set through the environment variable `TELEGRAM_ALLOWED_ID`. Ensure this ID and access to your Telegram account is kept secure and not shared with unauthorized individuals. Ensure access to the local machine is similarly restricted.

## Logging

Activity logging is enabled by default, with logs stored in `bot_activity.log`. These logs provide insights into bot usage and help with troubleshooting.

## Contributing

Contributions to enhance the bot's functionality or address issues are welcome, but I have no prior experience with managing contributions.

## License

This project is open-source and available under MIT License.

## Disclaimer

This bot is developed for educational and personal use. The author is not responsible for any misuse or damage caused by this software. Always ensure you have permission to execute code, run `.bat` files, and manipulate the target machine.
