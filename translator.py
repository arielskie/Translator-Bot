import os
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from deep_translator import GoogleTranslator
import logging

# --- Bot Configuration ---
# This line reads the secret token from the server's environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    # This line will make the bot crash if the token is missing, which helps with debugging
    raise ValueError("CRITICAL: No BOT_TOKEN found in environment variables. The bot cannot start.")

# --- Logging Setup ---
# This helps you see errors and status messages in the Zeabur logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Bot Command Handlers ---

async def start(update, context):
    """Sends a welcome message."""
    await update.message.reply_text(
        "Hello! I am your friendly translator bot.\n\n"
        "Send me any text, and I will translate it to English for you."
    )

async def help_command(update, context):
    """Sends a help message."""
    await update.message.reply_text(
        "Simply send any text message to get its English translation."
    )

# --- Translation Functionality ---

async def translate_text(update, context):
    """Translates the user's message."""
    user_message = update.message.text
    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(user_message)
        response = f"Translated to English:\n{translated_text}"
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"An error occurred during translation: {e}")
        await update.message.reply_text("Sorry, an error occurred while trying to translate.")

# --- Main Bot Execution ---

def main():
    """Starts the bot."""
    logger.info("Starting bot...")

    # This creates the bot application and disables the problematic job queue
    application = Application.builder().token(BOT_TOKEN).job_queue(None).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register the message handler for translation
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

    logger.info("Bot is now polling for messages...")
    # This starts the bot and keeps it running
    application.run_polling()

if __name__ == "__main__":
    main()
