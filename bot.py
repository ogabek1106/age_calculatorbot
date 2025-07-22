# 📦 Section 1: Imports
from datetime import datetime, date
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

# 🛡️ Section 2: Config
BOT_TOKEN = "8189011070:AAFHz_UeZ5udfmAW0X4OW2muqmYR_qMNb60"

# 🧠 Section 3: Age Calculator
def calculate_age(birth_str):
    try:
        # Try DD-MM-YYYY
        birth_date = datetime.strptime(birth_str, "%d-%m-%Y").date()
    except ValueError:
        try:
            # Try DDMMYYYY
            birth_date = datetime.strptime(birth_str, "%d%m%Y").date()
        except ValueError:
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

# 🔁 Update handler
async def handle_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    result = calculate_age(text)

    if result:
        y, m, d, wd = result
        await update.message.reply_text(
            f"🎉 You are {y} years, {m} months, and {d} days old!\n"
            f"🗓️ You were born on a {wd}."
        )
    else:
        await update.message.reply_text(
            "❌ Invalid format.\nTry: `21-07-2000` or `21072000`",
            parse_mode="Markdown"
        )

# 🚀 Section 5: Main App
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birthdate))
    app.run_polling()

if __name__ == "__main__":
    main()
