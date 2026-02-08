#!/usr/bin/env python3
"""
Telegram Stars Bot - Earn Telegram Stars
A complete bot system for earning stars through referrals, daily rewards, and channel subscriptions
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# =====================================================
# CONFIGURATION - Use environment variables for security
# =====================================================
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Bot token from BotFather
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))  # Admin Telegram ID

# =====================================================
# DATABASE STRUCTURE - Using JSON file for simplicity
# =====================================================
DATABASE_FILE = 'bot_database.json'

# =====================================================
# CONSTANTS - Bot settings and rewards
# =====================================================
REFERRAL_REWARD = 0.5  # Stars earned per referral
TASK_REWARD = 2.0  # Stars earned per completed task
DAILY_REWARD = 2.0  # Stars earned from daily gift
WITHDRAWAL_AMOUNTS = [50, 100, 200, 300]  # Available withdrawal amounts

# =====================================================
# TASKS CONFIGURATION - Channels/Groups to join
# =====================================================
TASKS = [
    {
        'id': 'task_1',
        'type': 'channel',
        'name': 'Example Channel 1',
        'link': 'https://t.me/example_channel',
        'chat_id': '@example_channel',  # Channel username or ID
        'reward': TASK_REWARD
    },
    {
        'id': 'task_2',
        'type': 'channel',
        'name': 'Example Channel 2',
        'link': 'https://t.me/example_channel2',
        'chat_id': '@example_channel2',
        'reward': TASK_REWARD
    },
    # Add more tasks here
]

# =====================================================
# LOGGING SETUP - Track bot activities
# =====================================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# =====================================================
# DATABASE MANAGEMENT - Load and save user data
# =====================================================

def load_database() -> Dict:
    """
    Load user database from JSON file
    Returns empty dict if file doesn't exist
    """
    try:
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading database: {e}")
        return {}

def save_database(data: Dict) -> None:
    """
    Save user database to JSON file
    Creates backup before saving
    """
    try:
        # Create backup
        if os.path.exists(DATABASE_FILE):
            backup_file = f"{DATABASE_FILE}.backup"
            with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                backup_data = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(backup_data)
        
        # Save new data
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving database: {e}")

def get_user_data(user_id: int) -> Dict:
    """
    Get user data from database
    Creates new user if doesn't exist
    """
    db = load_database()
    user_id_str = str(user_id)
    
    if user_id_str not in db:
        # Create new user with default values
        db[user_id_str] = {
            'user_id': user_id,
            'stars': 0.0,
            'referrals': [],
            'completed_tasks': [],
            'last_daily_reward': None,
            'referred_by': None,
            'username': None,
            'first_name': None,
            'join_date': datetime.now().isoformat(),
            'withdrawal_requests': []
        }
        save_database(db)
    
    return db[user_id_str]

def update_user_data(user_id: int, data: Dict) -> None:
    """
    Update user data in database
    """
    db = load_database()
    db[str(user_id)] = data
    save_database(db)

def add_stars(user_id: int, amount: float, reason: str = "") -> float:
    """
    Add stars to user account
    Returns new total
    """
    user_data = get_user_data(user_id)
    user_data['stars'] = round(user_data['stars'] + amount, 2)
    update_user_data(user_id, user_data)
    logger.info(f"Added {amount} stars to user {user_id}. Reason: {reason}")
    return user_data['stars']

# =====================================================
# KEYBOARD LAYOUTS - Main menu and navigation
# =====================================================

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Generate main menu keyboard with all options
    """
    keyboard = [
        [InlineKeyboardButton("⭐️ My Account", callback_data='account')],
        [InlineKeyboardButton("🎁 Daily Gift", callback_data='daily_gift')],
        [InlineKeyboardButton("📋 Tasks", callback_data='tasks')],
        [InlineKeyboardButton("👥 Referral", callback_data='referral')],
        [InlineKeyboardButton("💰 Withdraw", callback_data='withdraw')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard() -> InlineKeyboardMarkup:
    """
    Generate back button keyboard
    """
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)

def get_tasks_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Generate tasks keyboard with completion status
    """
    user_data = get_user_data(user_id)
    completed_tasks = user_data.get('completed_tasks', [])
    
    keyboard = []
    for task in TASKS:
        if task['id'] in completed_tasks:
            status = "✅"
        else:
            status = "❌"
        
        keyboard.append([
            InlineKeyboardButton(
                f"{status} {task['name']}",
                callback_data=f"task_{task['id']}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')])
    return InlineKeyboardMarkup(keyboard)

def get_withdrawal_keyboard() -> InlineKeyboardMarkup:
    """
    Generate withdrawal amounts keyboard
    """
    keyboard = []
    for amount in WITHDRAWAL_AMOUNTS:
        keyboard.append([
            InlineKeyboardButton(
                f"💎 {amount} Stars",
                callback_data=f"withdraw_{amount}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data='main_menu')])
    return InlineKeyboardMarkup(keyboard)

# =====================================================
# COMMAND HANDLERS - Bot commands
# =====================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command
    Process referral links and welcome new users
    """
    user = update.effective_user
    user_id = user.id
    
    # Update user info
    user_data = get_user_data(user_id)
    user_data['username'] = user.username
    user_data['first_name'] = user.first_name
    
    # Check for referral parameter
    if context.args and len(context.args) > 0:
        referrer_id = context.args[0]
        try:
            referrer_id = int(referrer_id)
            
            # Check if user hasn't been referred before and not self-referral
            if user_data['referred_by'] is None and referrer_id != user_id:
                user_data['referred_by'] = referrer_id
                
                # Add referral reward to referrer
                referrer_data = get_user_data(referrer_id)
                referrer_data['referrals'].append(user_id)
                add_stars(referrer_id, REFERRAL_REWARD, f"Referral from {user_id}")
                update_user_data(referrer_id, referrer_data)
                
                # Notify referrer
                try:
                    await context.bot.send_message(
                        chat_id=referrer_id,
                        text=f"🎉 Great news! @{user.username or user.first_name} joined using your referral link!\n"
                             f"💰 You earned {REFERRAL_REWARD} stars!"
                    )
                except Exception as e:
                    logger.error(f"Could not notify referrer {referrer_id}: {e}")
        except ValueError:
            pass
    
    update_user_data(user_id, user_data)
    
    # Welcome message with large star emoji
    welcome_text = (
        f"⭐️⭐️⭐️⭐️⭐️\n\n"
        f"🌟 **Welcome to Telegram Stars Bot!** 🌟\n\n"
        f"Hello, {user.first_name}! @{user.username or 'User'}\n\n"
        f"🎯 **Start earning Telegram Stars now!**\n\n"
        f"💫 **How to earn:**\n"
        f"🎁 Daily gifts - {DAILY_REWARD} stars\n"
        f"📋 Complete tasks - {TASK_REWARD} stars each\n"
        f"👥 Refer friends - {REFERRAL_REWARD} stars per referral\n\n"
        f"💰 **Withdraw your stars when you reach:**\n"
        f"{'  •  '.join([f'{amt}⭐️' for amt in WITHDRAWAL_AMOUNTS])}\n\n"
        f"🚀 Choose an option below to get started!"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command
    """
    help_text = (
        "📖 **Bot Help Guide**\n\n"
        "🌟 **Available Commands:**\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/account - View your account details\n\n"
        "💫 **How to Use:**\n\n"
        "1️⃣ **Daily Gift**: Claim your daily reward every 24 hours\n"
        "2️⃣ **Tasks**: Join channels/groups to earn stars\n"
        "3️⃣ **Referral**: Share your link and earn from referrals\n"
        "4️⃣ **Withdraw**: Request withdrawal when you have enough stars\n"
        "5️⃣ **Account**: Check your balance and statistics\n\n"
        "❓ **Need Support?** Contact admin for help!"
    )
    
    await update.message.reply_text(
        help_text,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

async def account_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /account command
    """
    user_id = update.effective_user.id
    await show_account(update, context, user_id)

# =====================================================
# CALLBACK HANDLERS - Button interactions
# =====================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle all button callbacks
    Routes to appropriate handler based on callback data
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    # Route to appropriate handler
    if data == 'main_menu':
        await show_main_menu(update, context)
    elif data == 'account':
        await show_account(update, context, user_id)
    elif data == 'daily_gift':
        await claim_daily_gift(update, context, user_id)
    elif data == 'tasks':
        await show_tasks(update, context, user_id)
    elif data.startswith('task_'):
        task_id = data.replace('task_', '')
        await handle_task(update, context, user_id, task_id)
    elif data == 'referral':
        await show_referral(update, context, user_id)
    elif data == 'withdraw':
        await show_withdraw(update, context, user_id)
    elif data.startswith('withdraw_'):
        amount = int(data.replace('withdraw_', ''))
        await process_withdrawal(update, context, user_id, amount)
    elif data == 'help':
        help_text = (
            "📖 **Bot Help Guide**\n\n"
            "🌟 **How to Use:**\n\n"
            "1️⃣ **Daily Gift**: Claim your daily reward every 24 hours\n"
            "2️⃣ **Tasks**: Join channels/groups to earn stars\n"
            "3️⃣ **Referral**: Share your link and earn from referrals\n"
            "4️⃣ **Withdraw**: Request withdrawal when you have enough stars\n"
            "5️⃣ **Account**: Check your balance and statistics\n\n"
            "❓ **Need Support?** Contact admin for help!"
        )
        await query.edit_message_text(
            help_text,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Display main menu
    """
    query = update.callback_query
    user = update.effective_user
    
    menu_text = (
        f"⭐️ **Telegram Stars Bot** ⭐️\n\n"
        f"Hello, {user.first_name}!\n\n"
        f"🎯 Choose an option below:"
    )
    
    await query.edit_message_text(
        menu_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

async def show_account(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """
    Display user account details
    Shows stars balance and referral count
    """
    user_data = get_user_data(user_id)
    
    stars = user_data['stars']
    referrals_count = len(user_data['referrals'])
    completed_tasks = len(user_data['completed_tasks'])
    join_date = datetime.fromisoformat(user_data['join_date']).strftime('%Y-%m-%d')
    
    account_text = (
        f"👤 **Your Account Details**\n\n"
        f"💰 **Balance:** {stars} ⭐️ Stars\n"
        f"👥 **Referrals:** {referrals_count} users\n"
        f"✅ **Completed Tasks:** {completed_tasks}/{len(TASKS)}\n"
        f"📅 **Member Since:** {join_date}\n\n"
        f"🎯 **Total Earned:**\n"
        f"  • From referrals: {referrals_count * REFERRAL_REWARD} ⭐️\n"
        f"  • From tasks: {completed_tasks * TASK_REWARD} ⭐️\n\n"
        f"💡 Keep earning stars and withdraw when ready!"
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            account_text,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            account_text,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )

async def claim_daily_gift(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """
    Handle daily gift claim
    Check 24-hour cooldown
    """
    query = update.callback_query
    user_data = get_user_data(user_id)
    
    last_claim = user_data.get('last_daily_reward')
    now = datetime.now()
    
    # Check if user can claim
    can_claim = True
    time_left = ""
    
    if last_claim:
        last_claim_dt = datetime.fromisoformat(last_claim)
        time_diff = now - last_claim_dt
        
        if time_diff < timedelta(hours=24):
            can_claim = False
            time_left_td = timedelta(hours=24) - time_diff
            hours = time_left_td.seconds // 3600
            minutes = (time_left_td.seconds % 3600) // 60
            time_left = f"{hours}h {minutes}m"
    
    if can_claim:
        # Give reward
        user_data['last_daily_reward'] = now.isoformat()
        add_stars(user_id, DAILY_REWARD, "Daily gift")
        update_user_data(user_id, user_data)
        
        message = (
            f"🎁 **Daily Gift Claimed!** 🎁\n\n"
            f"Congratulations! You received {DAILY_REWARD} ⭐️ stars!\n\n"
            f"💰 **New Balance:** {user_data['stars']} ⭐️\n\n"
            f"⏰ Come back in 24 hours for your next gift!"
        )
    else:
        message = (
            f"⏰ **Daily Gift Not Ready** ⏰\n\n"
            f"You already claimed your daily gift today!\n\n"
            f"⏳ **Time until next gift:** {time_left}\n\n"
            f"💡 Try completing tasks or referring friends meanwhile!"
        )
    
    await query.edit_message_text(
        message,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """
    Display available tasks
    """
    query = update.callback_query
    user_data = get_user_data(user_id)
    
    completed = len(user_data['completed_tasks'])
    total = len(TASKS)
    
    tasks_text = (
        f"📋 **Available Tasks** 📋\n\n"
        f"Complete tasks to earn {TASK_REWARD} ⭐️ stars each!\n\n"
        f"✅ **Completed:** {completed}/{total} tasks\n\n"
        f"💡 Click on a task to complete it:"
    )
    
    await query.edit_message_text(
        tasks_text,
        reply_markup=get_tasks_keyboard(user_id),
        parse_mode='Markdown'
    )

async def handle_task(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, task_id: str) -> None:
    """
    Handle task completion
    Check if user joined channel/group
    """
    query = update.callback_query
    user_data = get_user_data(user_id)
    
    # Find task
    task = next((t for t in TASKS if t['id'] == task_id), None)
    if not task:
        await query.answer("Task not found!")
        return
    
    # Check if already completed
    if task_id in user_data['completed_tasks']:
        await query.answer("✅ You already completed this task!")
        return
    
    # Show task details with join button
    task_text = (
        f"📋 **Task: {task['name']}**\n\n"
        f"💰 **Reward:** {task['reward']} ⭐️ stars\n\n"
        f"📝 **Instructions:**\n"
        f"1️⃣ Click 'Join Channel' button below\n"
        f"2️⃣ Join the channel/group\n"
        f"3️⃣ Click 'Verify' to check and get your reward\n\n"
        f"⚠️ Make sure you stay in the channel to receive your reward!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=task['link'])],
        [InlineKeyboardButton("✅ Verify", callback_data=f"verify_{task_id}")],
        [InlineKeyboardButton("🔙 Back to Tasks", callback_data='tasks')]
    ]
    
    await query.edit_message_text(
        task_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def verify_task_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Verify task completion
    Check channel membership
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    if not data.startswith('verify_'):
        return
    
    task_id = data.replace('verify_', '')
    
    # Find task
    task = next((t for t in TASKS if t['id'] == task_id), None)
    if not task:
        await query.answer("Task not found!")
        return
    
    user_data = get_user_data(user_id)
    
    # Check if already completed
    if task_id in user_data['completed_tasks']:
        await query.answer("✅ You already completed this task!")
        await show_tasks(update, context, user_id)
        return
    
    # Try to verify membership
    try:
        member = await context.bot.get_chat_member(task['chat_id'], user_id)
        
        # Check if user is a member
        if member.status in ['member', 'administrator', 'creator']:
            # Mark task as completed
            user_data['completed_tasks'].append(task_id)
            add_stars(user_id, task['reward'], f"Task {task_id}")
            update_user_data(user_id, user_data)
            
            success_text = (
                f"✅ **Task Completed!** ✅\n\n"
                f"Congratulations! You earned {task['reward']} ⭐️ stars!\n\n"
                f"💰 **New Balance:** {user_data['stars']} ⭐️\n\n"
                f"🎯 Complete more tasks to earn more stars!"
            )
            
            await query.edit_message_text(
                success_text,
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await query.answer("❌ You haven't joined the channel yet!", show_alert=True)
    except Exception as e:
        logger.error(f"Error verifying task: {e}")
        await query.answer(
            "⚠️ Could not verify membership. Make sure you joined the channel!",
            show_alert=True
        )

async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """
    Display referral information
    """
    query = update.callback_query
    user_data = get_user_data(user_id)
    
    bot_username = context.bot.username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"
    
    referrals_count = len(user_data['referrals'])
    total_earned = referrals_count * REFERRAL_REWARD
    
    referral_text = (
        f"👥 **Referral Program** 👥\n\n"
        f"💰 Earn {REFERRAL_REWARD} ⭐️ stars for each friend!\n\n"
        f"📊 **Your Statistics:**\n"
        f"  • Total Referrals: {referrals_count}\n"
        f"  • Stars Earned: {total_earned} ⭐️\n\n"
        f"🔗 **Your Referral Link:**\n"
        f"`{referral_link}`\n\n"
        f"📱 **How it works:**\n"
        f"1️⃣ Share your link with friends\n"
        f"2️⃣ They join using your link\n"
        f"3️⃣ You get {REFERRAL_REWARD} ⭐️ stars instantly!\n\n"
        f"💡 The more friends you invite, the more you earn!"
    )
    
    await query.edit_message_text(
        referral_text,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

async def show_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """
    Display withdrawal options
    """
    query = update.callback_query
    user_data = get_user_data(user_id)
    
    stars = user_data['stars']
    
    withdraw_text = (
        f"💰 **Withdraw Your Stars** 💰\n\n"
        f"💎 **Your Balance:** {stars} ⭐️ stars\n\n"
        f"📋 **Available Amounts:**\n"
    )
    
    for amount in WITHDRAWAL_AMOUNTS:
        if stars >= amount:
            withdraw_text += f"  ✅ {amount} stars\n"
        else:
            withdraw_text += f"  ❌ {amount} stars (Need {amount - stars} more)\n"
    
    withdraw_text += (
        f"\n💡 **Note:** Withdrawal requests are reviewed by admin.\n"
        f"⏰ Processing time: 24-48 hours\n\n"
        f"👇 Select amount to withdraw:"
    )
    
    await query.edit_message_text(
        withdraw_text,
        reply_markup=get_withdrawal_keyboard(),
        parse_mode='Markdown'
    )

async def process_withdrawal(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, amount: int) -> None:
    """
    Process withdrawal request
    Send notification to admin
    """
    query = update.callback_query
    user = update.effective_user
    user_data = get_user_data(user_id)
    
    stars = user_data['stars']
    
    # Check if user has enough stars
    if stars < amount:
        await query.answer(
            f"❌ Insufficient balance! You need {amount - stars} more stars.",
            show_alert=True
        )
        return
    
    # Deduct stars
    user_data['stars'] = round(stars - amount, 2)
    
    # Record withdrawal request
    withdrawal = {
        'amount': amount,
        'date': datetime.now().isoformat(),
        'status': 'pending'
    }
    user_data['withdrawal_requests'].append(withdrawal)
    update_user_data(user_id, user_data)
    
    # Send notification to admin
    admin_message = (
        f"💰 **New Withdrawal Request** 💰\n\n"
        f"👤 **User Details:**\n"
        f"  • Name: {user.first_name}\n"
        f"  • Username: @{user.username or 'Not set'}\n"
        f"  • User ID: `{user_id}`\n\n"
        f"💎 **Amount:** {amount} ⭐️ stars\n"
        f"📅 **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"⚠️ Please process this request."
    )
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Could not send message to admin: {e}")
    
    # Confirm to user
    success_text = (
        f"✅ **Withdrawal Request Submitted!** ✅\n\n"
        f"💎 **Amount:** {amount} ⭐️ stars\n"
        f"💰 **New Balance:** {user_data['stars']} ⭐️\n\n"
        f"📝 **Your request has been sent to admin.**\n"
        f"⏰ Processing time: 24-48 hours\n\n"
        f"💡 You will be notified once processed!"
    )
    
    await query.edit_message_text(
        success_text,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

# =====================================================
# MAIN FUNCTION - Start the bot
# =====================================================

def main() -> None:
    """
    Main function to start the bot
    Initialize handlers and start polling
    """
    # Check if token is provided
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is not set!")
        print("❌ Error: Please set BOT_TOKEN environment variable")
        return
    
    if not ADMIN_ID or ADMIN_ID == 0:
        logger.warning("ADMIN_ID environment variable is not set!")
        print("⚠️ Warning: ADMIN_ID not set. Withdrawal notifications won't work.")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("account", account_command))
    
    # Register callback handlers
    application.add_handler(CallbackQueryHandler(verify_task_callback, pattern='^verify_'))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    logger.info("🤖 Bot started successfully!")
    print("✅ Bot is running... Press Ctrl+C to stop")
    
    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
