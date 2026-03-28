import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid link")
        return

    try:
        await update.message.reply_text("Downloading video...")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, stream=True, timeout=10)

        if r.status_code != 200:
            await update.message.reply_text("Failed to download video ❌")
            return

        with open("video.mp4", "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        with open("video.mp4", "rb") as video:
            await update.message.reply_video(video=video)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()
