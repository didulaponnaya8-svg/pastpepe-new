import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"

PAPERS = {
    "physics_2021_s": {
        "name": "Physics 2021 සිංහල",
        "url": "https://drive.usercontent.google.com/download?id=1CYSZGiAl9gvpo62qH-1qiQvlN_N2odyA&export=download"
    },
    "physics_2020_s": {
        "name": "Physics 2020 සිංහල",
        "url": "https://drive.usercontent.google.com/download?id=1DEd8pqHnMCEzvdQX7mpfmBSmPm4IrNqL&export=download"
    },
    "physics_2019_s": {
        "name": "Physics 2019 සිංහල",
        "url": "https://drive.usercontent.google.com/download?id=1uIr8Kxv1TZVyasyKd5VoAjhiAD7PA3oo&export=download"
    },
    "physics_2018_s": {
        "name": "Physics 2018 සිංහල",
        "url": "https://drive.usercontent.google.com/download?id=1h0hQcB6RJuuLQ5ZwRLtyDPsY-pCogI3F&export=download"
    },
    "physics_2017_s": {
        "name": "Physics 2017 සිංහල",
        "url": "https://drive.usercontent.google.com/download?id=1OtltqF7TuP9VojH11pnun00MK7Jr1EV-&export=download"
    },
    "physics_2016_s": {
        "name": "Physics 2016 සිංහල",
        "url": "https://drive.usercontent.google.com/download?id=1elMWQUTtOpBMaXK9puNA090R1lrStlaY&export=download"
    }
}

def main_menu():
    keyboard = []
    # අලුත්ම Paper එක උඩට එන්න Sort කරපන්
    sorted_papers = dict(sorted(PAPERS.items(), key=lambda x: x[0], reverse=True))
    for key, data in sorted_papers.items():
        keyboard.append([InlineKeyboardButton(f"📘 {data['name']}", callback_data=key)])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *A/L Physics Past Papers සිංහල*\n*2016 - 2021*\n\nඕන අවුරුද්ද Select කරපන් 👇",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    paper = PAPERS[query.data]
    msg = await query.message.reply_text(f"⏳ {paper['name']} එවනවා...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(paper['url'], headers=headers, timeout=90)
        if r.status_code == 200 and 'application/pdf' in r.headers.get('Content-Type', ''):
            await query.message.reply_document(
                document=r.content,
                filename=f"{paper['name']}.pdf",
                caption=f"✅ {paper['name']}"
            )
            await msg.delete()
        else:
            await msg.edit_text(f"❌ Error {r.status_code}. Link එක Expired වෙන්න ඇති.")
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)[:100]}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
