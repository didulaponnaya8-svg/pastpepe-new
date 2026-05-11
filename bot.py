import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"
LOGO_FILE = "logo.png"

SUBJECTS = {
    "physics": {
        "name": "⚛️ Physics",
        "emoji": "⚛️",
        "years": "2016-2021",
        "papers": {
            "phy_2021": {"year": "2021", "id": "1ICLaJDoStL3J3wRDmPSJmqihX1tf6ORR"},
            "phy_2020": {"year": "2020", "id": "1jbpikdzS2tj1Q_X2tOiKYNVPYtZSg-tz"},
            "phy_2019": {"year": "2019", "id": "1N1I1-HzZdU1_YJ04I5GipyOcpQsn11uF"},
            "phy_2018": {"year": "2018", "id": "1CYSZGiAl9gvpo62qH-1qiQvlN_N2odyA"},
            "phy_2017": {"year": "2017", "id": "1yP8OWb5e0ce2dKGV_Yrb95WGozDOXIYY"},
            "phy_2016": {"year": "2016", "id": "14jLO0EA2U4g9O1HX_7bHEjt4cCWgh4LS"}
        }
    },
    "chemistry": {
        "name": "🧪 Chemistry",
        "emoji": "🧪",
        "years": "2016-2024",
        "papers": {
            "chem_2024": {"year": "2024", "id": "1i6JkE6gvFfa4I5Z8AiGFClmKDECCIifg"},
            "chem_2021": {"year": "2021", "id": "1nBr3BIdVWEgfOPNw1auOYdE6x9N-k6mu"},
            "chem_2020": {"year": "2020", "id": "1EjtW5p8HuOAo4QH5RBpHXi1FxvxZpk0I"},
            "chem_2019": {"year": "2019", "id": "1r8ugsWaHd7B1Rk56fr__hR1TCKhoLRIx"},
            "chem_2018": {"year": "2018", "id": "1FNKEb3ElNF-K830K93g87Q0uAvIqoXnm"},
            "chem_2017": {"year": "2017", "id": "1reDL1lZp5NCV6c0AE27Ewxy0OZqnJT1W"},
            "chem_2016": {"year": "2016", "id": "1XqsC_8__XMv6XhkABCIqBeu2FZk7wMzX"}
        }
    },
    "biology": {
        "name": "🧬 Biology",
        "emoji": "🧬",
        "years": "2016-2024",
        "papers": {
            "bio_2024": {"year": "2024", "id": "PASTE_BIO_2024_ID_HERE"},
            "bio_2021": {"year": "2021", "id": "PASTE_BIO_2021_ID_HERE"},
            "bio_2020": {"year": "2020", "id": "PASTE_BIO_2020_ID_HERE"},
            "bio_2019": {"year": "2019", "id": "PASTE_BIO_2019_ID_HERE"},
            "bio_2018": {"year": "2018", "id": "PASTE_BIO_2018_ID_HERE"},
            "bio_2017": {"year": "2017", "id": "PASTE_BIO_2017_ID_HERE"},
            "bio_2016": {"year": "2016", "id": "PASTE_BIO_2016_ID_HERE"}
        }
    }
}

def get_total_papers():
    return sum(len(sub["papers"]) for sub in SUBJECTS.values())

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
    row = []
    for sub_key, sub_data in SUBJECTS.items():
        count = len(sub_data["papers"])
        btn = InlineKeyboardButton(
            f"{sub_data['emoji']} {sub_key.title()} ({count})",
            callback_data=f"sub_{sub_key}"
        )
        row.append(btn)
        if len(row) == 2: # 2 buttons per row
            keyboard.append(row)
            row = []
    if row: # Odd number නම් last row එක
        keyboard.append(row)

    # Footer
    keyboard.append([InlineKeyboardButton(f"📊 Total Papers: {get_total_papers()}", callback_data="stats")])
    keyboard.append([InlineKeyboardButton("ℹ️ About", callback_data="about")])
    return InlineKeyboardMarkup(keyboard)

def papers_menu(subject_key):
    keyboard = []
    papers = SUBJECTS[subject_key]["papers"]
    sorted_papers = dict(sorted(papers.items(), reverse=True))

    row = []
    for paper_key, paper_data in sorted_papers.items():
        btn = InlineKeyboardButton(
            f"📘 {paper_data['year']}",
            callback_data=f"paper_{subject_key}_{paper_key}"
        )
        row.append(btn)
        if len(row) == 3: # 3 buttons per row for years
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("🔙 Back to Subjects", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = f"""
🌟 *A/L Past Papers Hub* 🌟
━━━━━━━━━━━━━━━━━━━━
⚛️ Physics | 🧪 Chemistry | 🧬 Biology
📚 *All Sinhala Medium*
━━━━━━━━━━━━━━━━━━━━
👇 *Select Subject Below*
    """
    try:
        with open(LOGO_FILE, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
    except FileNotFoundError:
        await update.message.reply_text(
            text=caption,
            parse_mode='Markdown',
            reply_markup=main_menu()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        caption = f"""
🌟 *A/L Past Papers Hub* 🌟
━━━━━━━━━━━━━━━━━━━━
⚛️ Physics | 🧪 Chemistry | 🧬 Biology
📚 *All Sinhala Medium*
━━━━━━━━━━━━━━━━━━━━
👇 *Select Subject Below*
        """
        await query.message.edit_caption(
            caption=caption,
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
        return

    if data == "about":
        await query.answer("Made with ❤️ for A/L Students by YourName", show_alert=True)
        return

    if data == "stats":
        stats = f"📊 *Bot Statistics*\n━━━━━━━━━━━━━━━━━━━━\n"
        for sub_data in SUBJECTS.values():
            stats += f"{sub_data['emoji']} {sub_data['name']}: {len(sub_data['papers'])} Papers\n"
        stats += f"━━━━━━━━━━━━━━━━━━━━\n🎯 *Total: {get_total_papers()} Papers*"
        await query.answer(stats, show_alert=True)
        return

    if data.startswith("sub_"):
        subject_key = data.split("_")[1]
        sub = SUBJECTS[subject_key]
        caption = f"""
{sub['emoji']} *{sub['name']} Past Papers*
━━━━━━━━━━━━━━━━━━━━
📅 *Years: {sub['years']}*
📚 *Total: {len(sub['papers'])} Papers*
━━━━━━━━━━━━━━━━━━━━
👇 *Select Year Below*
        """
        await query.message.edit_caption(
            caption=caption,
            parse_mode='Markdown',
            reply_markup=papers_menu(subject_key)
        )
        return

    if data.startswith("paper_"):
        _, subject_key, paper_key = data.split("_", 2)
        paper = SUBJECTS[subject_key]["papers"][paper_key]
        sub = SUBJECTS[subject_key]

        if "PASTE_BIO" in paper['id']:
            await query.message.reply_text("⚠️ *Bio Paper එක තාම Add කරලා නෑ*\nAdmin ට කියන්න Links දෙන්න!", parse_mode='Markdown')
            return

        msg = await query.message.reply_text(f"⏳ *Downloading...*\n{sub['emoji']} {sub['name']} {paper['year']}", parse_mode='Markdown')

        try:
            r = download_gdrive(paper['id'])
            content_type = r.headers.get('Content-Type', '')
            size_mb = int(r.headers.get('Content-Length', 0)) / 1024 / 1024

            if size_mb > 49:
                await msg.edit_text(
                    f"❌ *File Too Large*\n━━━━━━━━━━━━━━━━━━━━\n📄 {sub['name']} {paper['year']}\n💾 Size: {size_mb:.1f}MB\n⚠️ Telegram Limit: 50MB\n━━━━━━━━━━━━━━━━━━━━\n\n📎 *Direct Download:*\nhttps://drive.google.com/file/d/{paper['id']}/view",
                    parse_mode='Markdown'
                )
                return

            if 'application/pdf' in content_type or 'application/octet-stream' in content_type:
                await msg.edit_text(f"📤 *Uploading...*\n{sub['emoji']} {sub['name']} {paper['year']}", parse_mode='Markdown')
                await query.message.reply_document(
                    document=r.content,
                    filename=f"A/L_{sub['name']}_{paper['year']}_Sinhala.pdf",
                    caption=f"✅ *{sub['emoji']} {sub['name']} {paper['year']} Sinhala*\n━━━━━━━━━━━━━━━━━━━━\n📚 A/L Past Papers Hub\n💾 Size: {size_mb:.1f}MB",
                    parse_mode='Markdown'
                )
                await msg.delete()
            else:
                await msg.edit_text(
                    f"❌ *Download Failed*\n━━━━━━━━━━━━━━━━━━━━\nGDrive error\n\n📎 *Direct Link:*\nhttps://drive.google.com/file/d/{paper['id']}/view",
                    parse_mode='Markdown'
                )

        except Exception as e:
            await msg.edit_text(f"❌ *Error*\n━━━━━━━━━━━━━━━━━━━━\n{str(e)[:100]}", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot Started - Premium UI v3.0")
    app.run_polling()
