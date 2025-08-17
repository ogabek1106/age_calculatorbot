# 📦 Section 1: Imports
import os
from datetime import datetime, date
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

# 🛡️ Section 2: Config
BOT_TOKEN = os.getenv("BOT_TOKEN", "7753943408:AAETeACmEzACcAoIR8WDN732QcG2tB63EVA")

# 🧠 Section 3: Age Calculator
def calculate_age(birth_str):
    # 🔹 Handle 6-digit short format like 110602 → 11-06-2002
    if len(birth_str) == 6 and birth_str.isdigit():
        day = int(birth_str[:2])
        month = int(birth_str[2:4])
        year = int(birth_str[4:6])
        year += 2000 if year <= 49 else 1900  # 00–49 = 2000s, 50–99 = 1900s
        try:
            birth_date = date(year, month, day)
        except ValueError:
            return None
    else:
        # 🔹 Try full formats
        formats = ["%d-%m-%Y", "%d%m%Y", "%Y-%m-%d", "%Y%m%d"]
        for fmt in formats:
            try:
                birth_date = datetime.strptime(birth_str, fmt).date()
                break
            except ValueError:
                continue
        else:
            return None

    today = date.today()
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1
        prev_month = (today.month - 1) or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        days += (date(prev_year, prev_month % 12 + 1, 1) - date(prev_year, prev_month, 1)).days

    if months < 0:
        years -= 1
        months += 12

    weekday = birth_date.strftime("%A")
    return years, months, days, weekday

# 🤖 Section 4: Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! I can help you with two things:\n"
        "1️⃣ Calculate your age from your birthdate\n"
        "2️⃣ Calculate 1.7% and 2% of any number\n\n"
        "📅 Try sending:\n"
        "`21-07-2000` or `21072000` or `110602`\n"
        "💰 Or a number like: `150000`",
        parse_mode="Markdown"
    )

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # First, try calculating age
    result = calculate_age(text)
    if result:
        y, m, d, wd = result
        await update.message.reply_text(
            f"🎉 You are {y} years, {m} months, and {d} days old!\n"
            f"🗓️ You were born on a {wd}."
        )
        return

    # Then try percentage calculation
    if text.replace('.', '', 1).isdigit():
        number = float(text)
        percent_1_7 = round(number * 0.017, 2)
        percent_2 = round(number * 0.02, 2)
        after_1_7 = round(number - percent_1_7, 2)
        after_2 = round(number - percent_2, 2)

        await update.message.reply_text(
            f"📊 From {number}:\n"
            f"➕ 1.7% = {percent_1_7}\n"
            f"➖ {number} - 1.7% = {after_1_7}\n\n"
            f"➕ 2% = {percent_2}\n"
            f"➖ {number} - 2% = {after_2}"
        )
        return

    # If neither, show error
    await update.message.reply_text(
        "❌ Invalid input.\n\nTry:\n"
        "- Birthdate like `21-07-2000`, `21072000`, `110602`\n"
        "- Or number like `150000`",
        parse_mode="Markdown"
    )

# 🚀 Section 5: Launch
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))
    app.run_polling()

if __name__ == "__main__":
    main()
