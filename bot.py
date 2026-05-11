import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"

# Logo file එකේ නම. මේක උඹේ repo එකේ root folder එකේ තියෙන්න ඕන
LOGO_FILE = "logo.png"

SUBJECTS = {
    "physics": {
        "name": "⚛️ Physics",
        "years": "2016 - 2021",
        "papers": {
            "phy_2021": {"name": "2021 සිංහල", "id": "1ICLaJDoStL3J3wRDmPSJmqihX1tf6ORR"},
            "phy_2020": {"name": "2020 සිංහල", "id": "1jbpikdzS2tj1Q_X2tOiKYNVPYtZSg-tz"},
            "phy_2019": {"name": "2019 සිංහල", "id": "1N1I1-HzZdU1_YJ04I5GipyOcpQsn11uF"},
            "phy_2018": {"name": "2018 සිංහල", "id": "1CYSZGiAl9gvpo62qH-1qiQvlN_N2odyA"},
            "phy_2017": {"name": "2017 සිංහල", "id": "1yP8OWb5e0ce2dKGV_Yrb95WGozDOXIYY"},
            "phy_2016": {"name": "2016 සිංහල", "id": "14jLO0EA2U4g9O1HX_7bHEjt4cCWgh4LS"}
        }
    },
    "chemistry": {
        "name": "🧪 Chemistry",
        "years": "2016 - 2024",
        "papers": {
            "chem_2024": {"name": "2024 සිංහල", "id": "1i6JkE6gvFfa4I5Z8AiGFClmKDECCIifg"},
            "chem_2021": {"name": "2021 සිංහල", "id": "1nBr3BIdVWEgfOPNw1auOYdE6x9N-k6mu"},
            "chem_2020": {"name": "2020 සිංහල", "id": "1EjtW5p8HuOAo4QH5RBpHXi1FxvxZpk0I"},
            "chem_2019": {"name": "2019 සිංහල", "id": "1r8ugsWaHd7B1Rk56fr__hR1TCKhoLRIx"},
            "chem_2018": {"name": "2018 සිංහල", "id": "1FNKEb3ElNF-K830K93g87Q0uAvIqoXnm"},
            "chem_2017": {"name": "2017 සිංහල", "id": "1reDL1lZp5NCV6c0AE27Ewxy0OZqnJT1W"},
            "chem_2016": {"name": "2016 සිංහල", "id": "1XqsC_8__XMv6XhkABCIqBeu2FZk7wMzX"}
        }
    }
}

def download_gdrive(file_id):
    session = requests.Session()
    response = session.get("https://drive.google.com/uc", params={'export': 'download', 'id': file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
    if token:
        response = session.get("https://drive.google.com/uc", params={'export': 'download', 'id': file_id, 'confirm': token}, stream=True)
    return response

def main_menu():
    keyboard = []
    for sub_key, sub_data in SUBJECTS.items():
        keyboard.append([InlineKeyboardButton(sub_data['name'], callback_data=f"sub_{sub_key}")])
    return InlineKeyboardMarkup(keyboard)

def papers_menu(subject_key):
    keyboard = []
    papers = SUBJECTS[subject_key]["papers"]
    sorted_papers = dict(sorted(papers.items(), reverse=True))

    for paper_key, paper_data in sorted_papers.items():
        keyboard.append([InlineKeyboardButton(f"📘 {paper_data['name']}", callback_data=f"paper_{subject_key}_{paper_key}")])

    keyboard.append([InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = "📚 *A/L Past Papers Bot*\n*Physics | Chemistry*\n\nඕන Subject එක Select කරපන් 👇"
    # Local file එක Open කරනවා
    try:
        with open(LOGO_FILE, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
    except FileNotFoundError:
        # logo.png නැත්තන් Text එක විතරක් එවනවා
        await update.message.reply_text(
            text=caption + "\n\n⚠️ Logo file එක හම්බුනේ නෑ",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.message.edit_caption(
            caption="📚 *A/L Past Papers Bot*\n*Physics | Chemistry*\n\nඕන Subject එක Select කරපන් 👇",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
        return

    if data.startswith("sub_"):
        subject_key = data.split("_")[1]
        sub = SUBJECTS[subject_key]
        await query.message.edit_caption(
            caption=f"{sub['name']} *Past Papers*\n*{sub['years']}*\n\nඕන අවුරුද්ද Select කරපන් 👇",
            parse_mode='Markdown',
            reply_markup=papers_menu(subject_key)
        )
        return

    if data.startswith("paper_"):
        _, subject_key, paper_key = data.split("_", 2)
        paper = SUBJECTS[subject_key]["papers"][paper_key]
        sub_name = SUBJECTS[subject_key]['name']

        msg = await query.message.reply_text(f"⏳ {sub_name} {paper['name']} Download කරනවා...")

        try:
            r = download_gdrive(paper['id'])
            content_type = r.headers.get('Content-Type', '')
            size_mb = int(r.headers.get('Content-Length', 0)) / 1024 / 1024

            print(f"DEBUG: {paper['name']} | Type: {content_type} | Size: {size_mb:.2f}MB")

            if size_mb > 49:
                await msg.edit_text(
                    f"❌ {paper['name']} = {size_mb:.1f}MB\nTelegram 50MB Limit එක 😔\n\n📎 Direct Link:\nhttps://drive.google.com/file/d/{paper['id']}/view"
                )
                return

            if 'application/pdf' in content_type or 'application/octet-stream' in content_type:
                await msg.edit_text(f"📤 {sub_name} {paper['name']} Upload කරනවා...")
                await query.message.reply_document(
                    document=r.content,
                    filename=f"{sub_name}_{paper['name']}.pdf",
                    caption=f"✅ {sub_name} {paper['name']}"
                )
                await msg.delete()
            else:
                await msg.edit_text(
                    f"❌ GDrive එකෙන් PDF එක දුන්නෙ නෑ\n\n📎 Direct Link:\nhttps://drive.google.com/file/d/{paper['id']}/view"
                )

        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:200]}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot Started")
    app.run_polling()
