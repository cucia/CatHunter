# 🚀 Complete Setup Instructions

## Step 1: Extract Zip

Extract `cat_catcher_automation_complete.zip`

## Step 2: Create .env File

Go to `cat_catcher_user/` folder and create `.env`:

```
DISCORD_EMAIL=your_email@example.com
DISCORD_PASSWORD=your_password
TARGET_CHANNEL_ID=1395460222088253450
TARGET_SERVER_ID=1083346023470088232
```

**Replace:**
- `your_email@example.com` - Your Discord account email
- `your_password` - Your Discord account password

## Step 3: Build and Start

```bash
cd cat_catcher_user
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

## Step 4: Verify Success

You should see in logs:

```
✅ Login successful!
✅ Token saved to discord_token.json
✅ User Account Connected: YourName
✅ Channel found: #Cat-Play
✅ All checks passed! Starting monitoring...
🎯 Monitoring channel 1395460222088253450
🔍 Looking for Cat Bot messages
```

## Troubleshooting

### Login Failed: Invalid Credentials
- Check email is correct
- Check password is correct
- Password is case-sensitive

### Too Many Login Attempts
- Wait 15 minutes before trying again

### Channel Not Found
- Verify CHANNEL_ID is correct
- Make sure account has access

### Not catching images
- Check logs: `docker-compose logs -f`
- Wait 2 seconds per poll
- Verify Cat Bot is posting

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

## That's It!

Your automation is now running 24/7! 🐱
