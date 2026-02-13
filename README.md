# 🤖 Telegram Stars Bot - Complete Implementation

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)

A complete Telegram bot system for earning Telegram Stars through referrals, daily rewards, and channel subscriptions.

## ⭐️ Live Demo

Contact [@BotFather](https://t.me/BotFather) to create your own bot and deploy this code!

## 🌟 Features

### 💰 Multiple Earning Methods
- **🎁 Daily Gifts**: Claim 2 stars every 24 hours
- **📋 Task Completion**: Earn 2 stars for each channel/group subscription
- **👥 Referral System**: Get 0.5 stars for each friend who joins using your link

### 💎 Smart Withdrawal System
Users can withdraw their earned stars in these amounts:
- 50 Stars ⭐️
- 100 Stars ⭐️⭐️
- 200 Stars ⭐️⭐️⭐️
- 300 Stars ⭐️⭐️⭐️⭐️

All withdrawal requests are automatically sent to admin for quick approval.

### 📊 Comprehensive Account Management
- View total stars balance
- Track number of referrals
- Monitor completed tasks
- See detailed earning statistics
- Check join date and activity

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Telegram account
- Bot token from [@BotFather](https://t.me/BotFather)
- Your Telegram user ID from [@userinfobot](https://t.me/userinfobot)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aliiikrd/Whykur.git
   cd Whykur
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export ADMIN_ID="your_telegram_user_id"
   ```

   Or create a `.env` file (recommended):
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

   Or use the quick start script:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup and configuration guide
- **[README_AR.md](README_AR.md)** - Complete Arabic documentation (التوثيق العربي)
- **[DOCKER.md](DOCKER.md)** - Docker deployment guide
- **[DOCS.md](DOCS.md)** - Complete documentation index

## ⚙️ Configuration

### Adding Channels/Groups to Tasks

Edit the `TASKS` list in `bot.py`:

```python
TASKS = [
    {
        'id': 'task_1',
        'type': 'channel',
        'name': 'Your Channel Name',
        'link': 'https://t.me/your_channel',
        'chat_id': '@your_channel',
        'reward': TASK_REWARD
    },
    # Add more tasks here...
]
```

### Customizing Rewards

Modify these constants in `bot.py`:

```python
REFERRAL_REWARD = 0.5  # Stars per referral
TASK_REWARD = 2.0      # Stars per task
DAILY_REWARD = 2.0     # Daily gift stars
WITHDRAWAL_AMOUNTS = [50, 100, 200, 300]  # Available amounts
```

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
export BOT_TOKEN="your_token"
export ADMIN_ID="your_id"
docker-compose up -d
```

See [DOCKER.md](DOCKER.md) for complete Docker guide.

## 📋 Bot Commands

- `/start` - Start the bot and see welcome message
- `/help` - Display help information
- `/account` - View account details and statistics

## 🎯 User Flow

1. **Start**: User discovers bot (via referral or search)
2. **Welcome**: Beautiful welcome message with star emoji ⭐️
3. **Main Menu**: Clean interface with all options
4. **Earn Stars**:
   - Claim daily gift every 24 hours
   - Complete tasks by joining channels
   - Share referral link with friends
5. **Track Progress**: Check balance and statistics anytime
6. **Withdraw**: Request withdrawal when ready

## 🔒 Security Features

- ✅ Environment variables for sensitive data
- ✅ No hardcoded credentials anywhere
- ✅ Proper .gitignore configuration
- ✅ Database backup system before each save
- ✅ GitHub Secrets support for public repositories
- ✅ Input validation throughout
- ✅ Error logging and monitoring

## 📁 Project Structure

```
Whykur/
├── 📄 bot.py                      # Main bot (800+ lines, fully commented)
├── 📄 requirements.txt            # Python dependencies
├── 📄 start.sh                    # Quick start script
│
├── 📁 Documentation
│   ├── README.md                  # This file
│   ├── README_AR.md               # Arabic documentation
│   ├── SETUP.md                   # Setup guide
│   ├── DOCKER.md                  # Docker guide
│   └── DOCS.md                    # Documentation index
│
├── 📁 Configuration
│   ├── .env.example               # Environment template
│   ├── .gitignore                 # Git ignore rules
│   └── .dockerignore              # Docker ignore rules
│
├── 📁 Deployment
│   ├── Dockerfile                 # Docker image
│   ├── docker-compose.yml         # Docker Compose
│   └── telegram-bot.service       # Systemd service
│
└── 📁 Data (auto-generated)
    └── bot_database.json          # User data storage
```

## 🎨 Features Highlights

### ⭐️ Beautiful User Interface
- Large star emoji on welcome (⭐️)
- Clean menu structure with emojis
- Visual feedback for all actions (✅/❌)
- Progress tracking indicators
- Real-time notifications

### 🎁 Daily Rewards System
- 24-hour cooldown timer
- Countdown display for next claim
- Instant reward notification
- Persistent tracking

### 📋 Smart Task System
- Visual completion status
- Direct join buttons
- Automatic membership verification
- Immediate reward confirmation

### 👥 Powerful Referral System
- Unique referral link per user
- Instant reward on referral
- Automatic notification to referrer
- Complete statistics tracking

### 💰 Professional Withdrawal System
- Multiple amount options
- Balance validation
- Admin notification with full details
- Request history tracking

## 🛠️ Technical Details

### Technology Stack
- **Python**: 3.8+ compatible
- **Framework**: python-telegram-bot 20.7
- **Database**: JSON with auto-backup
- **Deployment**: Docker, Systemd, or direct

### Code Quality
- 800+ lines of well-documented code
- Comprehensive docstrings
- Detailed inline comments
- Modular design
- Complete error handling
- Extensive logging

### Database Structure
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

## 🐛 Troubleshooting

### Bot doesn't respond
- ✅ Check if BOT_TOKEN is set correctly
- ✅ Verify bot is running (check console)
- ✅ Ensure no firewall blocking

### Task verification fails
- ✅ Bot must be admin in the channel
- ✅ Check chat_id is correct (with @)
- ✅ Verify user actually joined

### Withdrawal notifications not received
- ✅ Check ADMIN_ID is your actual user ID
- ✅ Make sure you haven't blocked the bot
- ✅ Verify bot is running

See [SETUP.md](SETUP.md) for detailed troubleshooting.

## 📈 Scaling & Production

For production deployments:

1. **Database**: Switch to PostgreSQL or MySQL for better performance
2. **Caching**: Add Redis for faster responses
3. **Monitoring**: Use Sentry for error tracking
4. **Metrics**: Implement Prometheus + Grafana
5. **Load Balancing**: Deploy multiple instances
6. **Backups**: Automated daily database backups

## 🌍 Language Support

- **English**: Complete documentation and bot interface
- **Arabic**: Full documentation in [README_AR.md](README_AR.md)
- Bot messages: Currently in English (easily customizable)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues:
- Check the comprehensive documentation
- Review code comments
- Open an issue on GitHub
- Contact the admin

## 🎉 Credits

Built with ❤️ for the Telegram community.

Special thanks to:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) team
- Telegram Bot API developers
- All contributors and users

## ⭐️ Show Your Support

If you find this project useful:
- Give it a ⭐️ on GitHub
- Share with your friends
- Contribute to make it better
- Deploy your own bot and enjoy!

---

**Made with ❤️ by [aliiikrd](https://github.com/aliiikrd)**

⭐️ **Happy Botting!** ⭐️
