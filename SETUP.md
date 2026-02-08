# ⭐️ Quick Setup Guide

## 🚀 How to Run the Bot

### Method 1: Local Setup

1. **Get Bot Token**
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your User ID**
   - Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
   - Send any message
   - Copy your User ID (a number like: `123456789`)

3. **Set Environment Variables**
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export ADMIN_ID="your_user_id_here"
   ```

4. **Install and Run**
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```

   Or use the quick start script:
   ```bash
   ./start.sh
   ```

### Method 2: Using GitHub Secrets (Recommended for Public Repos)

1. **Fork/Clone this repository**

2. **Go to Repository Settings**
   - Click on "Settings" tab
   - Click on "Secrets and variables" → "Actions"
   - Click "New repository secret"

3. **Add Secrets**
   - Secret Name: `BOT_TOKEN`
     Value: Your bot token from BotFather
   
   - Secret Name: `ADMIN_ID`
     Value: Your Telegram user ID

4. **Deploy to Server**
   - Use the secrets in your deployment script
   - Example for manual server:
     ```bash
     export BOT_TOKEN="${{ secrets.BOT_TOKEN }}"
     export ADMIN_ID="${{ secrets.ADMIN_ID }}"
     python bot.py
     ```

## 🔧 Configuring Your Bot

### Adding Channels/Groups to Tasks

1. **Open `bot.py`**

2. **Find the `TASKS` section** (around line 40)

3. **Add your channels:**
   ```python
   TASKS = [
       {
           'id': 'task_1',  # Unique ID
           'type': 'channel',
           'name': 'My Awesome Channel',  # Display name
           'link': 'https://t.me/my_channel',  # Channel link
           'chat_id': '@my_channel',  # Username or ID
           'reward': TASK_REWARD
       },
       {
           'id': 'task_2',
           'type': 'channel',
           'name': 'My Second Channel',
           'link': 'https://t.me/my_channel2',
           'chat_id': '@my_channel2',
           'reward': TASK_REWARD
       },
   ]
   ```

### Getting Channel ID/Username

**For Public Channels:**
- Use the channel username (with @)
- Example: `@my_channel`

**For Private Channels:**
1. Add [@userinfobot](https://t.me/userinfobot) to your channel
2. Forward any message from the channel to the bot
3. Bot will show you the channel ID
4. Use the ID (example: `-1001234567890`)

### Important Notes

- **Bot must be admin** in channels to verify membership
- **Use exact username** including the @ symbol
- **Test each channel** before deploying to users

## 📱 Testing Your Bot

1. **Start the bot** (using one of the methods above)

2. **Open Telegram** and search for your bot

3. **Send `/start`** command

4. **Test all features:**
   - ✅ Daily gift claiming
   - ✅ Task completion
   - ✅ Referral link generation
   - ✅ Account statistics
   - ✅ Withdrawal request

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if BOT_TOKEN is set correctly
- Verify bot is running (check console output)
- Make sure no firewall is blocking

### Task verification fails
- Ensure bot is admin in the channel
- Check chat_id is correct
- Verify user actually joined the channel

### Withdrawal notification not received
- Check ADMIN_ID is set correctly
- Verify it's your actual Telegram user ID
- Make sure you haven't blocked the bot

### Database errors
- Check write permissions in the directory
- Ensure bot_database.json is not corrupted
- Use the .backup file if needed

## 📊 Monitoring

The bot logs all activities to console:
- User registrations
- Star earnings
- Task completions
- Withdrawal requests
- Errors and warnings

Use these logs to:
- Track bot performance
- Debug issues
- Monitor user activity
- Verify withdrawals

## 🎯 Best Practices

1. **Backup database regularly**
   ```bash
   cp bot_database.json bot_database_backup_$(date +%Y%m%d).json
   ```

2. **Monitor bot health**
   - Check logs daily
   - Verify task channels are active
   - Process withdrawals promptly

3. **Security**
   - Never share your bot token
   - Keep ADMIN_ID private
   - Don't commit .env file
   - Use GitHub Secrets for public repos

4. **User Experience**
   - Test all features before launch
   - Keep task channels active
   - Respond to user issues quickly
   - Update rewards as needed

## 🚀 Deployment Options

### Option 1: Local Machine
- Run on your computer
- Simple setup
- Must keep computer running

### Option 2: VPS/Cloud Server
- Rent a small VPS (DigitalOcean, AWS, etc.)
- Install Python and dependencies
- Run bot with systemd or PM2
- 24/7 availability

### Option 3: Heroku/Railway
- Use free tier for testing
- Easy deployment
- Automatic restarts
- Built-in logging

### Option 4: Docker
- Create Dockerfile
- Easy to deploy anywhere
- Consistent environment
- Scalable

## 📈 Scaling Up

When you have many users:

1. **Switch to PostgreSQL/MySQL**
   - Replace JSON database
   - Better performance
   - Data integrity

2. **Add Redis for caching**
   - Cache user data
   - Reduce database queries
   - Faster response times

3. **Use message queue**
   - Handle high traffic
   - Process tasks async
   - Better reliability

4. **Monitor with tools**
   - Sentry for errors
   - Prometheus for metrics
   - Grafana for visualization

## 🎉 You're Ready!

Your Telegram Stars Bot is now set up and ready to use!

For questions or issues, check the main README.md or open an issue on GitHub.

Happy botting! ⭐️
