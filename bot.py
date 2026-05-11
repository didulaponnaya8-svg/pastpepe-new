import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"

PAPERS = {
    "physics_2021_s": {"name": "Physics 2021 සිංහල", "id": "1ICLaJDoStL3J3wRDmPSJmqihX1tf6ORR"},
    "physics_2020_s": {"name": "Physics 2020 සිංහල", "id": "1jbpikdzS2tj1Q_X2tOiKYNVPYtZSg-tz"},
    "physics_2019_s": {"name": "Physics 2019 සිංහල", "id": "1N1I1-HzZdU1_YJ04I5GipyOcpQsn11uF"},
    "physics_2018_s": {"name": "Physics 2018 සිංහල", "id": "1CYSZGiAl9gvpo62qH-1qiQvlN_N2odyA"},
    "physics_2017_s": {"name": "Physics 2017 සිංහල", "id": "1yP8OWb5e0ce2dKGV_Yrb95WGozDOXIYY"},
    "physics_2016_s": {"name": "Physics 2016 සිංහල", "id": "14jLO0EA2U4g9O1HX_7bHEjt4cCWgh4LS"}
}

def download_gdrive(file_id):
    session = requests.Session()
    # First request
    response = session.get("https://drive.google.com/uc", params={'export': 'download', 'id': file_id}, stream=True)

    # Check if virus scan warning exists
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    # Second request with confirm token
    if token:
        response = session.get("https://drive.google.com/uc", params={'export': 'download', 'id': file_id, 'confirm': token}, stream=True)

    return response

def main_menu():
    keyboard = []
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
    msg = await query.message.reply_text(f"⏳ {paper['name']} Download කරනවා...")

    try:
        r = download_gdrive(paper['id'])
        content_type = r.headers.get('Content-Type', '')
        size_mb = int(r.headers.get('Content-Length', 0)) / 1024 / 1024

        print(f"DEBUG: {paper['name']} | Type: {content_type} | Size: {size_mb:.2f}MB")

        # Telegram 50MB Limit Check
        if size_mb > 49:
            await msg.edit_text(
                f"❌ {paper['name']} = {size_mb:.1f}MB\nTelegram 50MB Limit එක 😔\n\n📎 Direct Link:\nhttps://drive.google.com/file/d/{paper['id']}/view"
            )
            return

        # Check if actual PDF
        if 'application/pdf' in content_type or 'application/octet-stream' in content_type:
            await msg.edit_text(f"📤 {paper['name']} Upload කරනවා...")
            await query.message.reply_document(
                document=r.content,
                filename=f"{paper['name']}.pdf",
                caption=f"✅ {paper['name']}"
            )
            await msg.delete()
        else:
            await msg.edit_text(
                f"❌ GDrive එකෙන් PDF එක දුන්නෙ නෑ මචං\nType: {content_type}\n\n'Anyone with the link' දාලත් බැරි නම් File එක 100MB+ වෙන්න ඇති.\n\n📎 Direct Link:\nhttps://drive.google.com/file/d/{paper['id']}/view"
            )

    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)[:200]}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot Started")
    app.run_polling()
