import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8636197444:AAGSkenZi5vObBLibJc_aYAtM5jOT5Kd194"

def get_terabox_link(url):
    api = f"https://terabox-downloader-api.vercel.app/api?url={url}"
    res = requests.get(api).json()
    
    if res["status"] == "success":
        return res["download_link"]
    return None

def download_video(url, filename="video.mp4"):
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "terabox.com" in text:
        await update.message.reply_text("Downloading video... ⏳")

        link = get_terabox_link(text)

        if not link:
            await update.message.reply_text("Error ❌ Link process nahi hua")
            return

        try:
            file_path = download_video(link)

            await update.message.reply_video(video=open(file_path, "rb"))

        except Exception as e:
            await update.message.reply_text("File bada hai ❌\nDirect link 👇\n" + link)

    else:
        await update.message.reply_text("Sirf TeraBox link bhejo")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
