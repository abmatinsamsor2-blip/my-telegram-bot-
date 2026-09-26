from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

BOT_TOKEN = "توکن_ربات_را_اینجا_بگذار"

CHANNEL_USERNAME = "@My_Life_20_26"
CHANNEL_LINK = "https://t.me/My_Life_20_26"


async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        return member.status in ["member", "administrator", "creator"]

    except TelegramError:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    is_member = await check_membership(user_id, context)

    if not is_member:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ بررسی عضویت", callback_data="check")]
        ]

        await update.message.reply_text(
            "🔒 برای استفاده از ربات، ابتدا باید عضو کانال ما بشی.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "🎵 به ربات موزیک خوش اومدی!\n\n"
        "عضویتت تأیید شد ✅"
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    is_member = await check_membership(query.from_user.id, context)

    if is_member:
        await query.edit_message_text(
            "✅ عضویتت تأیید شد!\n"
            "حالا می‌تونی از ربات استفاده کنی 🎵"
        )
    else:
        await query.answer(
            "❌ هنوز عضو کانال نیستی.",
            show_alert=True
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(check, pattern="^check$"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
