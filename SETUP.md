# 🚀 Setup Instructions

## Quick Start (2 Minutes)

### 1. Create .env

Create a `.env` file in the root directory:

```
USER_TOKEN=your_user_token_here
TARGET_CHANNEL_ID=123456789012345678
BOT_ID=987654321098765432
TRIGGER_TEXT=Type "cat" to catch it!
RESPONSE_MESSAGE=cat
RESPONSE_DELAY=0
JITTER_ENABLED=false
JITTER_MAX=0
DEBUG_LOG_MESSAGES=false
```

### 2. Start Docker

```bash
docker-compose up -d
docker-compose logs -f
```

### 3. Done!

Watch for:
```
✅ Connected to Discord as YourUsername (ID: 123456789)
🎯 Listening for triggers in channel ID: 123456789012345678
```

Your bot is running and listening via WebSocket!

---

## Complete Setup Guide

### Step 1: Get Your User Token

**Warning:** Self-bots violate Discord's Terms of Service. Use at your own risk.

#### How to Get Your User Token:
1. Open Discord in your browser (desktop app won't work)
2. Press `F12` to open Developer Tools
3. Go to the "Network" tab
4. Type a message in any channel
5. Look for requests starting with "messages"
6. Click on one, go to "Headers"
7. Scroll to "Request Headers" → Find "authorization"
8. Copy the token value

### Step 2: Create .env File

Copy `.env.template` to `.env` and fill in:

```
USER_TOKEN=your_user_token_here
TARGET_CHANNEL_ID=123456789012345678
BOT_ID=987654321098765432
TRIGGER_TEXT=Type "cat" to catch it!
RESPONSE_MESSAGE=cat
LOG_LEVEL=INFO
RESPONSE_DELAY=0
JITTER_ENABLED=false
JITTER_MAX=0
DEBUG_LOG_MESSAGES=false
```

**Replace:**
- `your_user_token_here` - Your Discord user account token (see above for how to get it)
- `TARGET_CHANNEL_ID` - The channel ID where Cat Bot posts (optional)
- `BOT_ID` - The user ID of the Cat Bot that spawns cats

### Response Delay & Jitter Configuration

You can add a delay before the bot responds and optionally randomize it with jitter:

**`RESPONSE_DELAY`** (in seconds)
- Default: `0` (respond instantly)
- Example: `0.5` (wait 500ms before responding)

**`JITTER_ENABLED`** (true/false)
- Default: `false` (no jitter)
- Set to `true` to enable random jitter

**`JITTER_MAX`** (in seconds)
- Default: `0` (no jitter)
- Only used if `JITTER_ENABLED=true`
- Adds a random delay between 0 and `JITTER_MAX` to the base `RESPONSE_DELAY`
- Example: If `RESPONSE_DELAY=0.5` and `JITTER_MAX=0.3`, response will be between 0.5s and 0.8s

Example with delay and jitter:
```
RESPONSE_DELAY=0.5
JITTER_ENABLED=true
JITTER_MAX=0.5
```
This will respond between 0.5s and 1.0s randomly.

### Debug Logging

Set `DEBUG_LOG_MESSAGES=true` to print detailed logs explaining why messages are ignored (wrong channel, wrong bot ID, no trigger match). Useful for diagnosing issues when the bot appears to be "stuck".

### Selective Cat Catching

By default, the bot catches **all** cat types. You can enable/disable each cat and set a custom delay per type using `CATCH_<TYPE>` and `CATCH_<TYPE>_DELAY`. Optionally, enable jitter per type with `CATCH_<TYPE>_JITTER` (uses global `JITTER_MAX`).

Examples:
```
# Disable common cats, prioritize rare
CATCH_FINE=false
CATCH_NICE=false
CATCH_GOOD=false
CATCH_RARE=true

# Custom delay for Legendary and Mythic
CATCH_LEGENDARY=true
CATCH_LEGENDARY_DELAY=0.4
CATCH_MYTHIC=true
CATCH_MYTHIC_DELAY=0.5

# No jitter for ultra-rare types, jitter for others
CATCH_EIGHTBIT_JITTER=false
CATCH_ULTIMATE_JITTER=false
JITTER_ENABLED=true
JITTER_MAX=0.3
```

Available cat types (by rarity):
- **Common**: Fine (24.34%), Nice (18.26%), Good (12.17%), Rare (8.52%), Wild (6.69%), Baby (5.6%)
- **Uncommon**: Epic (4.87%), Sus (4.26%), Brave (3.65%), Rickroll (3.04%), Reverse (2.43%)
- **Rare**: Superior (1.95%), Trash (1.22%), Legendary (0.85%), Mythic (0.61%)
- **Ultra Rare**: 8bit (0.49%), Corrupt (0.37%), Professor (0.24%), Divine (0.19%), Real (0.12%), Ultimate (0.07%), eGirl (0.05%)
### Step 3: Build and Start

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

### Step 4: Verify Success

You should see in logs:

```
✅ Connected to Discord as YourUsername (ID: 123456789)
🎯 Listening for triggers in channel ID: 123456789012345678
```

When a cat appears:
```
✅ Responded with 'cat' to trigger from Cat Bot in #cat-play
```

---

## Troubleshooting

### Bot Not Connecting
- Check `USER_TOKEN` is correct
- Verify the token format is valid
- Make sure you're in the target server

### Bot Not Responding
- Check `BOT_ID` matches the Cat Bot's user ID
- Verify `TRIGGER_TEXT` matches the spawner's message
- Check logs: `docker-compose logs -f`
- Ensure bot can see the channel

### How to Get Bot ID
1. Enable Developer Mode in Discord (User Settings → Advanced)
2. Right-click the Cat Bot → Copy User ID
3. Paste into `BOT_ID` in `.env`

### How to Get Channel ID
1. Enable Developer Mode in Discord
2. Right-click the channel → Copy Channel ID
3. Paste into `TARGET_CHANNEL_ID` in `.env`

---

## Commands

```bash
# View live logs
docker-compose logs -f

# Stop automation
docker-compose down

# Restart
docker-compose restart

# Check status
docker-compose ps
```

---

## That's It!

Your automation is now running 24/7! 🐱
