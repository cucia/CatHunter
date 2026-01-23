import os
import logging
from dotenv import load_dotenv
import asyncio
import discord
import random

# Load environment
load_dotenv()

# Configuration from .env
USER_TOKEN = os.getenv('USER_TOKEN')  # User account token
CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
TRIGGER_TEXT = os.getenv('TRIGGER_TEXT', 'Type "cat" to catch it!')
RESPONSE_MESSAGE = os.getenv('RESPONSE_MESSAGE', 'cat')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'Cat Bot')
BOT_ID = os.getenv('BOT_ID')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DEBUG_LOG_MESSAGES = os.getenv('DEBUG_LOG_MESSAGES', 'false').lower() == 'true'

# Response delay configuration
RESPONSE_DELAY = float(os.getenv('RESPONSE_DELAY', '0'))  # Delay in seconds before sending response
JITTER_ENABLED = os.getenv('JITTER_ENABLED', 'false').lower() == 'true'  # Enable/disable jitter
JITTER_MAX = float(os.getenv('JITTER_MAX', '0'))  # Max jitter time in seconds

# Validate CHANNEL_ID if provided
try:
    CHANNEL_ID = int(CHANNEL_ID) if CHANNEL_ID else None
except ValueError:
    CHANNEL_ID = None

# Validate BOT_ID if provided
try:
    BOT_ID = int(BOT_ID) if BOT_ID else None
except ValueError:
    BOT_ID = None

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('automation.log'), logging.StreamHandler()]
)
logger = logging.getLogger('cat_catcher')

# Self-bot client (user account)
client = discord.Client()


@client.event
async def on_ready():
    logger.info(f"✅ Connected to Discord as {client.user} (ID: {client.user.id})")
    if CHANNEL_ID:
        logger.info(f"🎯 Listening for triggers in channel ID: {CHANNEL_ID}")
    else:
        logger.info("⚠️  No TARGET_CHANNEL_ID set; will respond in any channel where trigger appears.")
    # Log filter mode
    if BOT_ID:
        logger.info(f"🔎 Filter mode: BOT_ID={BOT_ID} (id match)")
    elif BOT_USERNAME:
        logger.info(f"🔎 Filter mode: BOT_USERNAME='{BOT_USERNAME}' (name match)")
    else:
        logger.info("🔎 Filter mode: Any bot messages (no specific bot configured)")


@client.event
async def on_message(message: discord.Message):
    # Ignore messages from ourselves
    if message.author.id == client.user.id:
        return

    # If a specific channel is configured, ignore others
    if CHANNEL_ID and message.channel.id != CHANNEL_ID:
        if DEBUG_LOG_MESSAGES:
            logger.debug(f"Ignoring message in channel {message.channel.id}; target is {CHANNEL_ID}")
        return

    # Prefer filtering by BOT_ID if provided; else by bot username; else only bots
    if BOT_ID:
        if message.author.id != BOT_ID:
            if DEBUG_LOG_MESSAGES:
                logger.debug(f"Ignoring author {message.author} (ID: {message.author.id}); BOT_ID filter = {BOT_ID}")
            return
    elif BOT_USERNAME:
        author_name = getattr(message.author, 'name', '') or getattr(message.author, 'display_name', '')
        if author_name.lower() != BOT_USERNAME.lower():
            if DEBUG_LOG_MESSAGES:
                logger.debug(f"Ignoring author {message.author} (name: '{author_name}'); BOT_USERNAME filter = '{BOT_USERNAME}'")
            return
    else:
        # Fallback: only consider messages from bots
        if not message.author.bot:
            if DEBUG_LOG_MESSAGES:
                logger.debug(f"Ignoring author {message.author} (ID: {message.author.id}); not a bot and no BOT filter configured")
            return

    # Check trigger text
    content = (message.content or '')
    if DEBUG_LOG_MESSAGES:
        preview = content.replace('\n', ' ')[:120]
        logger.debug(f"Candidate message from {message.author} (ID: {message.author.id}): '{preview}'")

    if TRIGGER_TEXT.lower() in content.lower():
        try:
            # Calculate delay with optional jitter
            delay = RESPONSE_DELAY
            if JITTER_ENABLED and JITTER_MAX > 0:
                jitter = random.uniform(0, JITTER_MAX)
                delay = RESPONSE_DELAY + jitter
            
            # Apply delay before sending response
            if delay > 0:
                logger.info(f"⏳ Waiting {delay:.3f}s before responding...")
                await asyncio.sleep(delay)
            
            await message.channel.send(RESPONSE_MESSAGE)
            logger.info(f"✅ Responded with '{RESPONSE_MESSAGE}' to trigger from {message.author} (ID: {message.author.id}) in #{message.channel}")
            if not BOT_ID and BOT_USERNAME:
                logger.info(f"📌 Detected spawner ID: {message.author.id}. Set BOT_ID={message.author.id} in .env and clear BOT_USERNAME to use ID-based filtering.")
        except Exception as e:
            logger.error(f"❌ Failed to send response: {e}")
    else:
        if DEBUG_LOG_MESSAGES:
            logger.debug("Trigger text not found in message; no action taken")


def run_bot():
    if not USER_TOKEN:
        logger.error('❌ USER_TOKEN not set in .env. Create a .env with USER_TOKEN=<your user token>')
        return

    try:
        client.run(USER_TOKEN)
    except Exception as e:
        logger.error(f"❌ Failed to run bot: {e}")


if __name__ == '__main__':
    run_bot()
