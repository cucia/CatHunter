# 🐱 Cat Catcher - Discord Self-Bot Automation

**Automate catching cats in Discord with a WebSocket-based self-bot!**

## 📦 What's Included

- ✅ WebSocket-based automation (instant detection, no polling)
- ✅ Docker-ready deployment
- ✅ 24/7 monitoring with auto-restart
- ✅ Full logging and documentation
- ✅ Simple self-bot setup

## 📁 Project Structure

```
CatHunter/
├── README.md              # This file
├── SETUP.md               # Setup instructions
├── automation.py          # Main bot code
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container config
├── docker-compose.yml     # Docker compose config
├── .env.template          # Environment template
├── .env                   # Your config (never commit!)
└── .gitignore             # Git ignore rules
```

## ⚡ Quick Start (2 Minutes)

### 1. Create .env

```bash
cp .env.template .env
```

Edit `.env`:
```
USER_TOKEN=your_user_token_here
TARGET_CHANNEL_ID=123456789012345678
BOT_ID=987654321098765432
```

### 2. Start

```bash
docker-compose up -d
docker-compose logs -f
```

### 3. Watch for Success

```
✅ Connected to Discord as YourUsername
🎯 Listening for triggers in channel ID: 123456789012345678
```

## 🎯 How It Works

```
Cat Bot posts message in channel
        ↓
Your bot receives instantly (WebSocket)
        ↓
YOUR bot responds "cat"
        ↓
YOU GET POINTS! 🏆
```

## ✨ Features

✅ **WebSocket-based** - Instant message detection, no polling delays
✅ **Self-bot support** - Works with user account tokens
✅ **ID-based filtering** - Respond only to specific bot (by ID or name)
✅ **Configurable delay & jitter** - Add random delays to avoid detection
✅ **Docker-ready** - Deploy anywhere Docker runs
✅ **24/7 operation** - Auto-restart on failure
✅ **Full logging** - Track what's happening
✅ **Customizable** - Trigger text, response message, delays via `.env`

## 🔒 Security

✅ Sensitive data in `.env` (not in code)
✅ `.env` is gitignored (never committed)
✅ Uses Discord Gateway (official WebSocket)
✅ ID-based filtering prevents impostors
✅ No credentials stored permanently

## ⚙️ Configuration

Key environment variables:
- `USER_TOKEN` — Your Discord user token
- `BOT_ID` — Spawner bot ID (ID-based filtering, most secure)
- `BOT_USERNAME` — Spawner bot name (fallback if no ID)
- `RESPONSE_DELAY` — Delay in seconds before responding (default: 0)
- `JITTER_ENABLED` — Add random jitter (true/false, default: false)
- `JITTER_MAX` — Max random delay in seconds (default: 0)

See [SETUP.md](SETUP.md) for full configuration guide.

## 📖 Documentation

See [SETUP.md](SETUP.md) for:
- Complete setup instructions
- Troubleshooting guide
- How to get your user token
- Docker commands reference

## ⚠️ Warning

Self-bots violate Discord's Terms of Service. Use at your own risk.

## 🎮 Common Commands

```bash
# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Check status
docker-compose ps
```

## 🚀 Ready?

```bash
cp .env.template .env
# Edit .env with your token and settings
docker-compose up -d
```

Happy catching! 🐱
