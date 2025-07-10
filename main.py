import logging
import requests
from telegram import Update, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === API KEYS ===
GEMINI_API_KEY = "AIzaSyCotKOw1sU0KavJxqZw07_3nExEkOSrK9E"
TELEGRAM_BOT_TOKEN = "7520921169:AAEjob5FlKcI5lWY7gX9e9Vn5J2kY66m6hA"

# === Logging ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Gemini Response Function ===
def get_gemini_response(user_input):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply.strip()
    except Exception as e:
        logger.error("Gemini API error: %s", e)
        return "❌ Sorry, Gemini couldn't respond right now. Please try again later."

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""👋 *Hey {user.first_name or 'there'}!*  
Welcome to 🤖 *Gemini AI Assistant* — your intelligent buddy for answers, ideas, and more!

💬 Just type anything — a doubt, question, or even a joke — and I’ll reply smartly like Google Gemini.

💡 Try me now!
"""
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

# === Handle All Text Messages ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text.strip()
    user_name = update.effective_user.first_name or "User"

    thinking_msg = await update.message.reply_text("🤔 Thinking...\n`Crafting a smart reply...`", parse_mode=ParseMode.MARKDOWN)

    response = get_gemini_response(user_question)

    await thinking_msg.delete()
    await update.message.reply_text(f"🧠 *Gemini says:*\n\n{response}", parse_mode=ParseMode.MARKDOWN)

    # Compliment + CTA
    compliment = f"""
✨ _Thanks for your curiosity, {user_name}! You're amazing._

🚀 Want a smart AI bot like this for *yourself or your business*?  
📩 [Let's Connect](https://t.me/Shreyansh9008)
"""
    await update.message.reply_text(compliment, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# === Main Function ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Gemini Telegram Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()