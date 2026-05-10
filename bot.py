import os
import json
import logging
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"
BOT_USERNAME = "@pastdlbbot_bot"

logging.basicConfig(level=logging.INFO)

# Subject එකට e-kalvi search URL map එක
EKALVI_SEARCH = {
    "physics": "https://e-kalvi.com/?s=2021+AL+Physics+Past+Paper+English",
    "chemistry": "https://e-kalvi.com/?s=2021+AL+Chemistry+Past+Paper+English",
    "biology": "https://e-kalvi.com/?s=2021+AL+Biology+Past+Paper+English",
}

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📘 A/L Physics", callback_data='sub_physics')],
        [InlineKeyboardButton("📗 A/L Chemistry", callback_data='sub_chemistry')],
        [InlineKeyboardButton("📙 A/L Biology", callback_data='sub_biology')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📚 *PastPaper LK Bot* 📚\n\n"
        f"✅ Live scraping from e-kalvi.com\n"
        f"✅ 100% Working PDFs\n\n"
        f"👇 Subject එකක් තෝරන්න",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('sub_'):
        subject = data.split('_')[1]
        msg = await query.message.reply_text(f"🔍 Searching {subject.title()} 2021 Paper...\n\nWait 10-15 seconds...")

        try:
            # 1. e-kalvi එකේ search කරලා PDF link එක හොයනවා
            search_url = EKALVI_SEARCH.get(subject)
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(search_url, headers=headers, timeout=30)
            soup = BeautifulSoup(r.text, 'html.parser')

            # 2. Download PDF button එකේ Google Drive link එක හොයනවා
            download_link = soup.find('a', href=lambda x: x and 'drive.google.com/uc?export=download' in x)

            if not download_link:
                await msg.edit_text("❌ Paper එක e-kalvi එකේ හොයාගන්න බැරි උනා. වෙන subject එකක් try කරන්න.")
                return

            pdf_url = download_link['href']

            # 3. Google Drive එකෙන් PDF එක download කරනවා
            await msg.edit_text("⏳ Downloading PDF from Google Drive...\n\nවිනාඩි 1ක් වගේ යයි...")
            pdf_response = requests.get(pdf_url, headers=headers, timeout=60)

            if pdf_response.status_code == 200:
                pdf_file = BytesIO(pdf_response.content)
                pdf_file.name = f"AL_{subject.title()}_2021.pdf"

                await query.message.reply_document(
                    document=pdf_file,
                    caption=f"✅ A/L {subject.title()} 2021\n\n📥 Download Complete!\n📡 Source: e-kalvi.com\n\nBot: {BOT_USERNAME}"
                )
                await msg.delete()
            else:
                await msg.edit_text(f"❌ Google Drive download failed. Status: {pdf_response.status_code}")

        except Exception as e:
            logging.error(f"Error: {e}")
            await msg.edit_text(f"❌ Error: {str(e)}\n\nServer slow වෙන්න පුලුවන්. ආයෙ try කරන්න.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is polling... 100% Online ✅")
    app.run_polling()
