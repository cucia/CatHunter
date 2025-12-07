# 🐱 Discord User Account Automation - #Cat-Play

Automate your Discord account to catch cat images in **#Cat-Play** channel 24/7!

## ⚡ Quick Start

### 1️⃣ Create .env File

In this folder, create `.env`:

```
DISCORD_EMAIL=your_email@example.com
DISCORD_PASSWORD=your_password
TARGET_CHANNEL_ID=1395460222088253450
TARGET_SERVER_ID=1083346023470088232
```

### 2️⃣ Start Docker

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

### 3️⃣ Watch Logs

You should see:
```
✅ Login successful!
✅ User Account Connected: YourName
✅ Channel found: #Cat-Play
✅ All checks passed! Starting monitoring...
```

## 🎯 How It Works

- Logs in with your credentials
- Saves token locally
- Monitors #Cat-Play every 2 seconds
- Detects Cat Bot images
- Auto-responds with "cat"
- YOU get the points! 🏆

## 🎮 Commands

```bash
# Start
docker-compose up -d

# View logs live
docker-compose logs -f

# Stop
docker-compose down

# Check if running
docker-compose ps

# View catches
docker-compose logs | grep "🐱"
```

## 🔒 Security

✅ Credentials in .env (not in code)
✅ .env is gitignored (never committed)
✅ Token saved locally
✅ Uses Discord official API

**Happy catching! 🐱**
