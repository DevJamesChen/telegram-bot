# OpenAI Telegram Assistant

This is a simple Python script that uses OpenAI's GPT-3 API to power an AI assistant on Telegram. It can respond to user messages with generated text and provide the current time in Istanbul, Seoul, and Seattle when the "/remoteworktime" command is issued.

## Prerequisites

To use this script, you will need the following:

- An OpenAI API key
- A Telegram bot token

## Setup

1. Clone this repository and navigate to the root directory.
2. Create a virtual environment: `python3 -m venv venv`.
3. Activate the virtual environment: `source venv/bin/activate`.
4. Install the dependencies: `pip install -r requirements.txt`.
5. Create a file called `.env` in the root directory and add your OpenAI API key and Telegram bot token:

OPENAI_API_KEY=<your OpenAI API key>
TELEGRAM_BOT_TOKEN=<your Telegram bot token>

6. Run the script: `python3 main.py`

## Usage

Once the script is running, you can interact with the AI assistant by sending messages to the Telegram bot. If you mention the bot's name in a group or supergroup chat, it will respond with generated text based on your message. If you send the "/remoteworktime" command, the bot will respond with the current time in Istanbul, Seoul, and Seattle.

## Contributing

If you would like to contribute to this project, feel free to open a pull request or submit an issue.
