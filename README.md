# About
Telegram bot for tracking the number of current job vacancies on the robota.ua website.

# Installation
For correct operation, you need to install Python version 3.10+ with the "ADD TO PATH" option.
Open the command line in the project folder and install the necessary libraries using the command:
`pip install -r requirements.txt`

# Configuration
In the `config.json` file:

1. Insert your bot token in the `bot_token` field, which can be obtained from `@BotFather` in Telegram.
2. Insert the keyword for searching on the "robota.ua" website in the `parsing_keyword` field.
3. In the `at_00:00` field, leave the value `true` if you want to receive the number of vacancies at 00:00, 01:00, 02:00, etc.
4. In the `at_00:00` field, set the value to `false` if you want to receive the number of vacancies every hour after the bot starts.

# Launch
Open the command line in the folder with the main.py file and enter the command:
`python .\main.py`
