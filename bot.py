from datetime import datetime
import os
import openai
import logging
from dotenv import load_dotenv
import pytz
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set your OpenAI API key and Telegram bot token
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY


async def set_commands(bot):
    """Set the bot's commands"""
    commands = [BotCommand(
        "remoteworktime", "Get the current time in Istanbul, Seoul, and Seattle"),
    ]

    await bot.set_my_commands(commands)


async def remote_work_time_command(update, context):
    """Send the current time in Istanbul, Seoul, and Seattle when the command /remoteworktime is issued."""
    # Define the timezones for Istanbul, Seoul, and Seattle
    istanbul_tz = pytz.timezone('Europe/Istanbul')
    seoul_tz = pytz.timezone('Asia/Seoul')
    seattle_tz = pytz.timezone('America/Los_Angeles')

    # Get the current time in each timezone
    istanbul_time = datetime.now(istanbul_tz).strftime('%I:%M:%S %p')
    seoul_time = datetime.now(seoul_tz).strftime('%I:%M:%S %p')
    seattle_time = datetime.now(seattle_tz).strftime('%I:%M:%S %p')

    # Construct the response message
    response = f"The current time in Istanbul is {istanbul_time}.\n"
    response += f"The current time in Seoul is {seoul_time}.\n"
    response += f"The current time in Seattle is {seattle_time}."

    # Send the response message
    await update.message.reply_text(response)


async def gpt_query(prompt: str) -> str:
    # Check if the user is asking about the model
    if "what model" in prompt.lower():
        return "I am an AI assistant."

    # Test for davinci-003 model.
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    # Get the last message from the assistant in the response messages
    assistant_message = response['choices'][0]['text']
    return assistant_message.strip()


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user message and generate a response."""
    user_message = update.message.text
    chat_type = update.effective_chat.type

    if chat_type == 'group' or chat_type == 'supergroup':
        # Check if bot is mentioned in message
        bot_username = context.bot.username
        if f"@{bot_username}" in user_message:
            # Remove bot's name from message
            user_message = user_message.replace(f"@{bot_username}", "").strip()
            prompt = f"{user_message}\n\nGPT-3:"
            response = await gpt_query(prompt)
            await update.message.reply_text(response)
    else:
        prompt = user_message
        response = await gpt_query(prompt)
        await update.message.reply_text(response)


if __name__ == '__main__':
    # Set up the bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Set the bot's commands with application:
    application.add_handler(CommandHandler(
        "remoteworktime", remote_work_time_command))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

# # Run the bot
application.run_polling(1.0)
