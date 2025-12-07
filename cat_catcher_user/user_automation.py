import httpx
import asyncio
import logging
import os
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Setup logging - SUPPRESS httpx DEBUG logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CHANNEL_ID = os.getenv('TARGET_CHANNEL_ID')
SERVER_ID = os.getenv('TARGET_SERVER_ID')
EMAIL = os.getenv('DISCORD_EMAIL')
PASSWORD = os.getenv('DISCORD_PASSWORD')
RESPONSE_MESSAGE = "cat"
TRIGGER_TEXT = 'Type "cat" to catch it!'

# Token storage
TOKEN_FILE = 'discord_token.json'

# Discord API base
API_BASE = "https://discord.com/api/v10"

def load_token():
    """Load token from file if exists"""
    if Path(TOKEN_FILE).exists():
        try:
            with open(TOKEN_FILE, 'r') as f:
                data = json.load(f)
                return data.get('token')
        except:
            pass
    return None

def save_token(token):
    """Save token to file"""
    with open(TOKEN_FILE, 'w') as f:
        json.dump({'token': token}, f)
    logger.info(f"✅ Token saved to {TOKEN_FILE}")

async def login_with_credentials():
    """Login with email and password to get token"""
    logger.info("🔐 Logging in with Discord credentials...")
    
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "login": EMAIL,
                "password": PASSWORD
            }
            
            response = await client.post(
                f"{API_BASE}/auth/login",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                if token:
                    logger.info("✅ Login successful!")
                    save_token(token)
                    return token
                else:
                    logger.error("❌ No token received from login")
                    return None
            
            elif response.status_code == 401:
                logger.error("❌ Login failed: Invalid credentials")
                return None
            
            elif response.status_code == 429:
                logger.error("❌ Too many login attempts. Try again later.")
                return None
            
            else:
                logger.error(f"❌ Login failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Login error: {e}")
            return None

async def validate_token(token):
    """Validate token by fetching user info"""
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE}/users/@me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('username', 'Unknown')
                user_id = user_data.get('id', 'Unknown')
                logger.info(f"✅ User Account Connected: {username} (ID: {user_id})")
                return True, user_data
            
            elif response.status_code == 401:
                logger.error("❌ Token Invalid or Expired")
                return False, None
            
            else:
                logger.error(f"❌ Validation error: {response.status_code}")
                return False, None
                
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False, None

async def get_channel_info(token):
    """Get channel information"""
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_BASE}/channels/{CHANNEL_ID}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                channel_data = response.json()
                channel_name = channel_data.get('name', 'Unknown')
                logger.info(f"✅ Channel found: #{channel_name}")
                return True
            
            else:
                logger.error(f"❌ Channel not found: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error getting channel: {e}")
            return False

async def send_message(token, content: str):
    """Send message to channel"""
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "content": content,
                "tts": False
            }
            
            response = await client.post(
                f"{API_BASE}/channels/{CHANNEL_ID}/messages",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"✅✅✅ SENT MESSAGE: '{content}' ✅✅✅")
                return True
            
            else:
                logger.error(f"❌ Failed to send: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return False

async def monitor_channel(token):
    """Monitor channel for new messages and trigger text"""
    last_message_id = None
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    logger.info(f"🎯 Monitoring channel {CHANNEL_ID}")
    logger.info(f"🔍 Looking for trigger: '{TRIGGER_TEXT}'")
    logger.info(f"📝 Response message: '{RESPONSE_MESSAGE}'")
    logger.info("=" * 60)
    
    while True:
        try:
            async with httpx.AsyncClient() as client:
                # Get recent messages
                url = f"{API_BASE}/channels/{CHANNEL_ID}/messages?limit=10"
                response = await client.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    messages = response.json()
                    
                    # Initialize last_message_id on first run
                    if last_message_id is None and messages:
                        last_message_id = int(messages[0]['id'])
                        logger.info(f"✅ Started tracking from message ID: {last_message_id}")
                        await asyncio.sleep(2)
                        continue
                    
                    # Process messages in reverse order (oldest first)
                    for message in reversed(messages):
                        msg_id = int(message['id'])
                        
                        # Skip if we've seen this message
                        if last_message_id and msg_id <= last_message_id:
                            continue
                        
                        # Update last seen ID
                        last_message_id = msg_id
                        
                        # Author info
                        author = message.get('author', {})
                        author_name = author.get('username', '')
                        
                        # Only process messages from Cat Bot
                        if author_name == "Cat Bot":
                            content = message.get('content', '')
                            
                            # Check if message contains the trigger text
                            if TRIGGER_TEXT.lower() in content.lower():
                                logger.info("")
                                logger.info("🐱🐱🐱 TRIGGER DETECTED! RESPONDING NOW! 🐱🐱🐱")
                                logger.info(f"   Message: {content[:100]}")
                                logger.info("")
                                
                                # Send response immediately
                                await send_message(token, RESPONSE_MESSAGE)
                
                elif response.status_code == 401:
                    logger.error("❌ Token expired! Please restart the container.")
                    return False
                
        except Exception as e:
            logger.error(f"⚠️  Error in monitoring: {e}")
        
        # Poll every 1 seconds
        await asyncio.sleep(1)

async def main():
    """Main automation"""
    logger.info("🚀 Starting Cat Catcher Automation...")
    logger.info("=" * 60)
    
    # Validate configuration
    if not CHANNEL_ID:
        logger.error("❌ TARGET_CHANNEL_ID not set in .env!")
        return
    
    if not SERVER_ID:
        logger.error("❌ TARGET_SERVER_ID not set in .env!")
        return
    
    # Get token
    token = load_token()
    
    if not token:
        # Try to login with credentials
        if not EMAIL or not PASSWORD:
            logger.error("❌ No saved token and no credentials in .env!")
            return
        
        token = await login_with_credentials()
        
        if not token:
            logger.error("❌ Failed to obtain token")
            return
    
    # Validate token
    logger.info("🔐 Validating token...")
    is_valid, user_data = await validate_token(token)
    
    if not is_valid:
        logger.error("❌ Token is invalid. Trying to login again...")
        
        if EMAIL and PASSWORD:
            token = await login_with_credentials()
            if not token:
                return
            
            is_valid, user_data = await validate_token(token)
            if not is_valid:
                logger.error("❌ Still invalid after login. Check credentials.")
                return
        else:
            logger.error("❌ No credentials to re-login.")
            return
    
    # Check channel access
    logger.info("🔍 Checking channel access...")
    if not await get_channel_info(token):
        logger.error("❌ Cannot access channel.")
        return
    
    logger.info("✅ All checks passed! Starting monitoring...")
    logger.info("=" * 60)
    
    # Start monitoring
    try:
        await monitor_channel(token)
    except KeyboardInterrupt:
        logger.info("\n⏹️  Stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
