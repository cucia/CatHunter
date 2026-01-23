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

# Selective cat catching - individual enable/disable and custom delays per cat type
CAT_TYPES = [
    'Fine', 'Nice', 'Good', 'Rare', 'Wild', 'Baby', 'Epic', 'Sus',
    'Brave', 'Rickroll', 'Reverse', 'Superior', 'Trash', 'Legendary',
    'Mythic', '8bit', 'Corrupt', 'Professor', 'Divine', 'Real',
    'Ultimate', 'eGirl'
]

# Build cat config dictionary from environment
CAT_CONFIG = {}
for cat_type in CAT_TYPES:
    env_base = cat_type.upper().replace('8BIT', 'EIGHTBIT')
    env_key = f"CATCH_{env_base}"
    delay_key = f"CATCH_{env_base}_DELAY"
    jitter_key = f"CATCH_{env_base}_JITTER"
    
    enabled = os.getenv(env_key, 'true').lower() == 'true'  # Default: catch all
    delay = float(os.getenv(delay_key, str(RESPONSE_DELAY)))  # Default: use global delay
    
    # Per-cat jitter: use CATCH_<TYPE>_JITTER if set, else fall back to global JITTER_ENABLED
    raw_jitter = os.getenv(jitter_key)
    if raw_jitter is not None:
        jitter_enabled = raw_jitter.lower() == 'true'
    else:
        jitter_enabled = JITTER_ENABLED
    
    CAT_CONFIG[cat_type.lower()] = {
        'enabled': enabled,
        'delay': delay,
        'jitter_enabled': jitter_enabled
    }

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
    # Log catch mode
    enabled_cats = [cat.title() for cat, config in CAT_CONFIG.items() if config['enabled']]
    disabled_cats = [cat.title() for cat, config in CAT_CONFIG.items() if not config['enabled']]
    
    if len(enabled_cats) == len(CAT_CONFIG):
        logger.info("🎯 Catch mode: ALL cats enabled")
    elif len(enabled_cats) == 0:
        logger.info("⚠️  Catch mode: NO cats enabled (bot will not respond)")
    else:
        logger.info(f"🎯 Catch mode: {len(enabled_cats)}/{len(CAT_CONFIG)} types enabled")
        if len(disabled_cats) <= 10:
            logger.info(f"   Disabled: {', '.join(disabled_cats)}")


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

    # Extract cat type from message (e.g., "Nice cat has appeared!" -> "Nice")
    cat_type = extract_cat_type(content)
    
    # Check if we should catch this type of cat
    if cat_type:
        cat_key = cat_type.lower()
        if cat_key in CAT_CONFIG:
            if not CAT_CONFIG[cat_key]['enabled']:
                if DEBUG_LOG_MESSAGES:
                    logger.debug(f"Skipping {cat_type} cat; CATCH_{cat_type.upper()}=false")
                else:
                    logger.info(f"⏭️  Skipped {cat_type} cat (disabled)")
                return
            # Use per-cat delay
            cat_delay = CAT_CONFIG[cat_key]['delay']
        else:
            # Unknown cat type, use global delay
            cat_delay = RESPONSE_DELAY
    else:
        # Couldn't determine cat type, use global delay
        cat_delay = RESPONSE_DELAY

    if TRIGGER_TEXT.lower() in content.lower():
        try:
            # Calculate delay with optional jitter
            delay = cat_delay
            
            # Use per-cat jitter settings if available
            if cat_type and cat_type.lower() in CAT_CONFIG:
                jitter_enabled = CAT_CONFIG[cat_type.lower()]['jitter_enabled']
            else:
                jitter_enabled = JITTER_ENABLED
            
            if jitter_enabled and JITTER_MAX > 0:
                jitter = random.uniform(0, JITTER_MAX)
                delay = cat_delay + jitter
            
            # Apply delay before sending response
            if delay > 0:
                logger.info(f"⏳ Waiting {delay:.3f}s before responding...")
                await asyncio.sleep(delay)
            
            await message.channel.send(RESPONSE_MESSAGE)
            logger.info(f"✅ Caught {cat_type} cat! Responded with '{RESPONSE_MESSAGE}'")
            if not BOT_ID and BOT_USERNAME:
                logger.info(f"📌 Detected spawner ID: {message.author.id}. Set BOT_ID={message.author.id} in .env and clear BOT_USERNAME to use ID-based filtering.")
        except Exception as e:
            logger.error(f"❌ Failed to send response: {e}")
    else:
        if DEBUG_LOG_MESSAGES:
            logger.debug("Trigger text not found in message; no action taken")


def extract_cat_type(content: str) -> str:
    """Extract cat type from message like 'Nice cat has appeared!' -> 'Nice'"""
    for cat_type in CAT_TYPES:
        if cat_type.lower() in content.lower():
            return cat_type
    
    return None


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
