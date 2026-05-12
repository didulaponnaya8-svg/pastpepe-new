import os
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"
LOGO_FILE = "logo.png" # Render එකට logo.png Upload කරපන්
ADMIN_ID = 123456789 # << උඹේ ID එක දාපන් @userinfobot එකෙන්
USERS_FILE = "users.json"

SUBJECTS = {
    "physics": {
        "name": "⚛️ Physics", "emoji": "⚛️", "years": "2016-2021",
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
        "name": "🧪 Chemistry", "emoji": "🧪", "years": "2016-2024",
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
        "name": "🧬 Biology", "emoji": "🧬", "years": "2011-2023",
        "papers": {
            "bio_2023": {"year": "2023", "id": "1m46B0XwT0wILto45xmfJbLVyVO7SotwI"},
            "bio_2022": {"year": "2022", "id": "1Vple1rcjSM_ZCB2hFpHi2g26ZwOmnqFD"},
            "bio_2021": {"year": "2021", "id": "1-w0U7c_rP_sUzTwNXJjiuCvAoHIc3IJg"},
            "bio_2020": {"year": "2020", "id": "1tO8s6-fFa9QEoHVF14LDeSWq9CTKV2Vg"},
            "bio_2019": {"year": "2019", "id": "1OcaqyWatw1E9AU6gsbhyDOJSUyEnXOFL"},
            "bio_2018": {"year": "2018", "id": "1qd3D35yz-TglQ_3yJDcqPm7f7Vj8Uxjx"},
            "bio_2017": {"year": "2017", "id": "1fCEvtD07JA32TwP_pudB31mptU-MVE3-"},
            "bio_2016": {"year": "2016", "id": "1U7fnfUZ6wsslU7L7eAxZXXTgEjViKdEm"},
            "bio_2015": {"year": "2015", "id": "1uyfLx5tIoaEkZuu9-S9iJXkoK1w5YH5u"},
            "bio_2013": {"year": "2013", "id": "1US231ibZFSYwVqEQWmfFXrI2KYumY-S1"},
            "bio_2011": {"year": "2011", "id": "1dsc1-TXuXySD2Tb26pZafqZLoZUL3DBy"}
        }
    },
    "maths": {
        "name": "📐 Combined Maths", "emoji": "📐", "years": "2012-2023",
        "papers": {
            "maths_2023": {"year": "2023", "id": "1UwCR0d--pDEGwdiK9hwuIMRnSYpiw-7Z"},
            "maths_2022": {"year": "2022", "id": "19F-Q8jYfIwGXvVO9SCpeTlqN003Syq3A"},
            "maths_2021": {"year": "2021", "id": "1TuVDuV_WPV8lIdTI1_U_B4e7XVMECv5d"},
            "maths_2020": {"year": "2020", "id": "14VFJKE0wPuurBzJnY2_yVYq8st6mCRr7"},
            "maths_2019": {"year": "2019", "id": "1-Mp8RFORpf1vXw_-547olWS5Ema-NNKO"},
            "maths_2018": {"year": "2018", "id": "1DILTRLHAsasTPEeO31_aOvP63xvUA1jD"},
            "maths_2017": {"year": "2017", "id": "1FH8POD5jAEP1zlMV-Df6d4YiTtwkUR55"},
            "maths_2016": {"year": "2016", "id": "1x5X4GOnkM56waRoSjpZW21ijNf62i39v"},
            "maths_2015": {"year": "2015", "id": "1WPASU4XjshbDAcjDN08O452oJ3J3ZdOu"},
            "maths_2014": {"year": "2014", "id": "1USBVSnWN3HoKz0N_c1j2w7x0xmtA_436"},
            "maths_2013": {"year": "2013", "id": "1rV1FfRrLZViSyhdBscYiwU3Z0HRBJGqc"},
            "maths_2012": {"year": "2012", "id": "1KnfBXqXDt8XdQgo-fJ23N3dXVYM3iNnS"}
        }
    }
}

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)

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
        btn = InlineKeyboardButton(f"{sub_data['emoji']} {sub_key.title()} ({count})", callback_data=f"sub_{sub_key}")
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(f"📊 Total Papers: {get_total_papers()}", callback_data="stats")])
    return InlineKeyboardMarkup(keyboard)

def papers_menu(subject_key):
    keyboard = []
    papers = SUBJECTS[subject_key]["papers"]
    sorted_papers = dict(sorted(papers.items(), reverse=True))
    row = []
    for paper_key, paper_data in sorted_papers.items():
        btn = InlineKeyboardButton(f"📘 {paper_data['year']}", callback_data=f"paper_{subject_key}_{paper_key}")
        row.append(btn)
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back to Subjects", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    caption = f"""
🌟 *𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰* 🌟
━━━━━━━━━━━━━━━━━━━━
⚛️ Physics | 🧪 Chemistry | 🧬 Biology | 📐 Maths
📚 *A/L Past Papers Sinhala Medium*
━━━━━━━━━━━━━━━━━━━━
👇 *Select Subject Below*
    """
    try:
        with open(LOGO_FILE, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=caption, parse_mode='Markdown', reply_markup=main_menu())
    except FileNotFoundError:
        await update.message.reply_text(text=caption, parse_mode='Markdown', reply_markup=main_menu())

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id!= ADMIN_ID:
        await update.message.reply_text("❌ *Admin Only Command*", parse_mode='Markdown')
        return
    if not context.args:
        await update.message.reply_text("📢 *Usage:*\n`/broadcast Your Message Here`", parse_mode='Markdown')
        return
    message = " ".join(context.args)
    users = load_users()
    await update.message.reply_text(f"📤 *Broadcasting to {len(users)} users...*", parse_mode='Markdown')
    success = 0
    failed = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 *Announcement*\n━━━━━━━━━━━━━━━━━━━━\n{message}\n━━━━━━━━━━━━━━━━━━━━\n_𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰_", parse_mode='Markdown')
            success += 1
        except:
            failed += 1
    await update.message.reply_text(f"✅ *Broadcast Complete*\n━━━━━━━━━━━━━━━━━━━━\n📤 Sent: {success}\n❌ Failed: {failed}", parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        caption = f"""
🌟 *𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰* 🌟
━━━━━━━━━━━━━━━━━━━━
⚛️ Physics | 🧪 Chemistry | 🧬 Biology | 📐 Maths
📚 *A/L Past Papers Sinhala Medium*
━━━━━━━━━━━━━━━━━━━━
👇 *Select Subject Below*
        """
        await query.message.edit_caption(caption=caption, parse_mode='Markdown', reply_markup=main_menu())
        return

    if data == "stats":
        stats = f"📊 *Bot Statistics*\n━━━━━━━━━━━━━━━━━━━━\n"
        for sub_data in SUBJECTS.values():
            stats += f"{sub_data['emoji']} {sub_data['name']}: {len(sub_data['papers'])} Papers\n"
        stats += f"━━━━━━━━━━━━━━━━━━━━\n🎯 *Total: {get_total_papers()} Papers*\n👥 *Users: {len(load_users())}*"
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
        await query.message.edit_caption(caption=caption, parse_mode='Markdown', reply_markup=papers_menu(subject_key))
        return

    if data.startswith("paper_"):
        _, subject_key, paper_key = data.split("_", 2)
        paper = SUBJECTS[subject_key]["papers"][paper_key]
        sub = SUBJECTS[subject_key]
        msg = await query.message.reply_text(f"⏳ *Downloading...*\n{sub['emoji']} {sub['name']} {paper['year']}", parse_mode='Markdown')
        try:
            r = download_gdrive(paper['id'])
            size_mb = int(r.headers.get('Content-Length', 0)) / 1024
            if size_mb > 49:
                await msg.edit_text(f"❌ *File Too Large*\n━━━━━━━━━━━━━━━━━━━━\n📄 {sub['name']} {paper['year']}\n💾 Size: {size_mb:.1f}MB\n\n📎 *Direct Download:*\nhttps://drive.google.com/file/d/{paper['id']}/view", parse_mode='Markdown')
                return
            await msg.edit_text(f"📤 *Uploading...*\n{sub['emoji']} {sub['name']} {paper['year']}", parse_mode='Markdown')
            await query.message.reply_document(document=r.content, filename=f"A/L_{sub['name']}_{paper['year']}_Sinhala.pdf", caption=f"✅ *{sub['emoji']} {sub['name']} {paper['year']} Sinhala*\n💾 Size: {size_mb:.1f}MB\n\n_𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰_", parse_mode='Markdown')
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ *Error:* {str(e)[:100]}", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot Started - Lanka Paper Hub v5.0")
    app.run_polling()
