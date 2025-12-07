# ⚡ Quick Start (2 Minutes)

## 1. Create .env

In `cat_catcher_user/` create `.env`:

```
DISCORD_EMAIL=your_email@example.com
DISCORD_PASSWORD=your_password
TARGET_CHANNEL_ID=1395460222088253450
TARGET_SERVER_ID=1083346023470088232
```

## 2. Start

```bash
cd cat_catcher_user
docker-compose up -d
docker-compose logs -f
```

## 3. Done!

Watch for:
```
✅ Login successful!
✅ All checks passed! Starting monitoring...
```

🎉 Your automation is running!
