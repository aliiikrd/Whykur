# ⭐️ Telegram Stars Bot

A complete Telegram bot system for earning Telegram Stars through referrals, daily rewards, and channel subscriptions.

## 🌟 Features

### 💰 Earning Methods
- **Daily Gifts**: Claim 2 stars every 24 hours
- **Task Completion**: Earn 2 stars for each channel/group subscription
- **Referral System**: Get 0.5 stars for each friend who joins using your link

### 💎 Withdrawal System
Users can withdraw their earned stars in these amounts:
- 50 Stars
- 100 Stars
- 200 Stars
- 300 Stars

All withdrawal requests are sent to admin for approval.

### 📊 Account Management
- View total stars balance
- Track number of referrals
- See completed tasks
- Check earning statistics

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- A Telegram account
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd webapp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file or set environment variables:
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export ADMIN_ID="your_telegram_user_id"
   ```

   Or use GitHub Secrets for deployment:
   - Go to Repository Settings → Secrets
   - Add `BOT_TOKEN` and `ADMIN_ID` as secrets

4. **Run the bot**
   ```bash
   python bot.py
   ```

## ⚙️ Configuration

### Setting Up Tasks

Edit the `TASKS` list in `bot.py` to add your channels/groups:

```python
TASKS = [
    {
        'id': 'task_1',
        'type': 'channel',
        'name': 'Your Channel Name',
        'link': 'https://t.me/your_channel',
        'chat_id': '@your_channel',  # Channel username or ID
        'reward': TASK_REWARD
    },
    # Add more tasks here
]
```

### Getting Channel ID

1. Add [@userinfobot](https://t.me/userinfobot) to your channel
2. Forward a message from the channel to the bot
3. The bot will show you the channel ID

### Getting Your User ID

1. Message [@userinfobot](https://t.me/userinfobot)
2. It will reply with your user ID
3. Use this as `ADMIN_ID`

## 📋 Bot Commands

- `/start` - Start the bot and see main menu
- `/help` - Display help information
- `/account` - View account details and statistics

## 🎯 User Flow

1. **Start**: User starts the bot (optionally via referral link)
2. **Welcome**: User receives welcome message with menu
3. **Earn Stars**:
   - Claim daily gift (every 24 hours)
   - Complete tasks (join channels)
   - Refer friends
4. **Check Balance**: View account statistics
5. **Withdraw**: Request withdrawal when minimum reached

## 🔒 Security Features

- Environment variables for sensitive data
- No hardcoded credentials
- Database backup system
- Error logging and monitoring
- Input validation

## 📁 Project Structure

```
webapp/
├── bot.py                 # Main bot code with all features
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── bot_database.json     # User data (auto-generated)
```

## 🗄️ Database Structure

The bot uses a JSON file for data storage with this structure:

```json
{
  "user_id": {
    "user_id": 123456789,
    "stars": 10.5,
    "referrals": [987654321],
    "completed_tasks": ["task_1", "task_2"],
    "last_daily_reward": "2024-01-01T12:00:00",
    "referred_by": null,
    "username": "example_user",
    "first_name": "John",
    "join_date": "2024-01-01T10:00:00",
    "withdrawal_requests": []
  }
}
```

## 🎨 Features Highlights

### ⭐️ Visual Effects
- Large star emoji on welcome
- Emoji indicators for all features
- Clean and organized menu structure
- Progress tracking with visual feedback

### 🎁 Daily Rewards
- 24-hour cooldown timer
- Countdown display for next claim
- Instant reward notification

### 📋 Task System
- Visual completion status (✅/❌)
- Join button with direct link
- Automatic membership verification
- Reward confirmation

### 👥 Referral System
- Unique referral link for each user
- Instant reward on referral
- Notification to referrer
- Statistics tracking

### 💰 Withdrawal System
- Multiple withdrawal amounts
- Balance validation
- Admin notification with user details
- Request tracking

## 🛠️ Customization

### Changing Rewards

Edit these constants in `bot.py`:

```python
REFERRAL_REWARD = 0.5  # Stars per referral
TASK_REWARD = 2.0      # Stars per task
DAILY_REWARD = 2.0     # Daily gift stars
WITHDRAWAL_AMOUNTS = [50, 100, 200, 300]  # Available amounts
```

### Adding More Features

The code is well-commented and modular. You can easily add:
- More task types
- Different reward mechanisms
- Admin commands
- Statistics and leaderboards
- Bonus events

## 📝 Notes

- Bot stores data in `bot_database.json` (auto-created)
- Automatic backup before each save
- All timestamps in ISO format
- Supports unlimited users
- Logging enabled for debugging

## ⚠️ Important

1. **Never commit `.env` file** - It contains sensitive data
2. **Keep bot token secret** - Anyone with token can control your bot
3. **Backup database regularly** - User data is valuable
4. **Test tasks before deploying** - Ensure channels are accessible
5. **Monitor admin notifications** - Process withdrawals promptly

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available for personal and commercial use.

## 📞 Support

For issues or questions:
- Check the code comments for detailed explanations
- Review the help section in the bot
- Contact the admin for assistance

---

Made with ❤️ for the Telegram community

⭐️ **Star this repo if you find it useful!** ⭐️
