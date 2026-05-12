import telebot
from telebot import types
import json
import os
from datetime import datetime

# ============= CONFIG =============
BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"
ADMIN_ID = 8231869218

bot = telebot.TeleBot(BOT_TOKEN)
STATS_FILE = 'stats.json'

# ============= SUBJECTS + PAPERS =============
SUBJECTS = {
    "physics": {
        "name": "⚛️ Physics", "emoji": "⚛️", "years": "2016-2021",
        "papers": {
            "physics_2021": {"year": "2021", "id": "PHYSICS_2021_FILE_ID"},
            "physics_2020": {"year": "2020", "id": "PHYSICS_2020_FILE_ID"},
            "physics_2019": {"year": "2019", "id": "PHYSICS_2019_FILE_ID"},
            "physics_2018": {"year": "2018", "id": "PHYSICS_2018_FILE_ID"},
            "physics_2017": {"year": "2017", "id": "PHYSICS_2017_FILE_ID"},
            "physics_2016": {"year": "2016", "id": "PHYSICS_2016_FILE_ID"}
        }
    },
    "chemistry": {
        "name": "🧪 Chemistry", "emoji": "🧪", "years": "2016-2024",
        "papers": {
            "chemistry_2024": {"year": "2024", "id": "CHEMISTRY_2024_FILE_ID"},
            "chemistry_2023": {"year": "2023", "id": "CHEMISTRY_2023_FILE_ID"},
            "chemistry_2022": {"year": "2022", "id": "CHEMISTRY_2022_FILE_ID"},
            "chemistry_2021": {"year": "2021", "id": "CHEMISTRY_2021_FILE_ID"},
            "chemistry_2020": {"year": "2020", "id": "CHEMISTRY_2020_FILE_ID"},
            "chemistry_2019": {"year": "2019", "id": "CHEMISTRY_2019_FILE_ID"},
            "chemistry_2018": {"year": "2018", "id": "CHEMISTRY_2018_FILE_ID"},
            "chemistry_2017": {"year": "2017", "id": "CHEMISTRY_2017_FILE_ID"},
            "chemistry_2016": {"year": "2016", "id": "CHEMISTRY_2016_FILE_ID"}
        }
    },
    "biology": {
        "name": "🧬 Biology", "emoji": "🧬", "years": "2011-2023",
        "papers": {
            "biology_2023": {"year": "2023", "id": "BIOLOGY_2023_FILE_ID"},
            "biology_2022": {"year": "2022", "id": "BIOLOGY_2022_FILE_ID"},
            "biology_2021": {"year": "2021", "id": "BIOLOGY_2021_FILE_ID"},
            "biology_2020": {"year": "2020", "id": "BIOLOGY_2020_FILE_ID"},
            "biology_2019": {"year": "2019", "id": "BIOLOGY_2019_FILE_ID"},
            "biology_2018": {"year": "2018", "id": "BIOLOGY_2018_FILE_ID"},
            "biology_2017": {"year": "2017", "id": "BIOLOGY_2017_FILE_ID"},
            "biology_2016": {"year": "2016", "id": "BIOLOGY_2016_FILE_ID"},
            "biology_2015": {"year": "2015", "id": "BIOLOGY_2015_FILE_ID"},
            "biology_2014": {"year": "2014", "id": "BIOLOGY_2014_FILE_ID"},
            "biology_2013": {"year": "2013", "id": "BIOLOGY_2013_FILE_ID"},
            "biology_2012": {"year": "2012", "id": "BIOLOGY_2012_FILE_ID"},
            "biology_2011": {"year": "2011", "id": "BIOLOGY_2011_FILE_ID"}
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

# ============= STATS FUNCTIONS =============
def load_stats():
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"users": {}, "downloads": {}, "total_downloads": 0, "total_users": 0}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

def add_user(user_id, username):
    stats = load_stats()
    user_id = str(user_id)
    if user_id not in stats["users"]:
        stats["users"][user_id] = {
            "username": username,
            "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "downloads": 0
        }
        stats["total_users"] += 1
        save_stats(stats)

def log_download(user_id, paper_key):
    stats = load_stats()
    user_id = str(user_id)
    stats["total_downloads"] += 1
    if user_id in stats["users"]:
        stats["users"][user_id]["downloads"] += 1
    if paper_key not in stats["downloads"]:
        stats["downloads"][paper_key] = 0
    stats["downloads"][paper_key] += 1
    save_stats(stats)

# ============= KEYBOARDS =============
def main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    total = 0
    for sub_key, sub_data in SUBJECTS.items():
        count = len(sub_data["papers"])
        total += count
        buttons.append(types.InlineKeyboardButton(
            f"{sub_data['emoji']} {sub_data['name'].split()[-1]} ({count})",
            callback_data=f"sub_{sub_key}"
        ))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton(f"📊 Total Papers: {total}", callback_data="stats_total"))
    if user_id == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("📈 Admin Statistics", callback_data="admin_stats"))
    return markup

def subject_menu(sub_key):
    markup = types.InlineKeyboardMarkup(row_width=3)
    subject = SUBJECTS[sub_key]
    papers = sorted(subject["papers"].items(), key=lambda x: x[1]["year"], reverse=True)
    buttons = []
    for paper_key, paper_data in papers:
        buttons.append(types.InlineKeyboardButton(
            f"📄 {paper_data['year']}",
            callback_data=f"paper_{sub_key}_{paper_key}"
        ))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu"))
    return markup

def paper_menu(sub_key, paper_key):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬇️ Download PDF", callback_data=f"dl_{sub_key}_{paper_key}"))
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"sub_{sub_key}"))
    return markup

# ============= HANDLERS =============
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id, message.from_user.username or message.from_user.first_name)
    text = f"🇱🇰 *𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛* 🇱🇰\n\n"
    text += f"Hello {message.from_user.first_name}! 👋\n"
    text += f"A/L Past Papers 2011-2024\n\n"
    text += f"*Select a Subject:*"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=main_menu(message.from_user.id))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    add_user(call.from_user.id, call.from_user.username or call.from_user.first_name)

    if call.data == "main_menu":
        text = f"🇱🇰 *𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛* 🇱🇰\n\n*Select a Subject:*"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode='Markdown', reply_markup=main_menu(call.from_user.id))

    elif call.data.startswith("sub_"):
        sub_key = call.data.replace("sub_", "")
        subject = SUBJECTS[sub_key]
        text = f"{subject['emoji']} *{subject['name']}*\n"
        text += f"Years: {subject['years']}\n"
        text += f"Papers: {len(subject['papers'])}\n\n"
        text += f"*Select Year:*"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode='Markdown', reply_markup=subject_menu(sub_key))

    elif call.data.startswith("paper_"):
        _, sub_key, paper_key = call.data.split("_", 2)
        subject = SUBJECTS[sub_key]
        paper = subject["papers"][paper_key]
        text = f"{subject['emoji']} *{subject['name']} - {paper['year']}*\n\n"
        text += f"📄 A/L Past Paper {paper['year']}\n"
        text += f"✅ Ready to Download"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                            parse_mode='Markdown', reply_markup=paper_menu(sub_key, paper_key))

    elif call.data.startswith("dl_"):
        _, sub_key, paper_key = call.data.split("_", 2)
        subject = SUBJECTS[sub_key]
        paper = subject["papers"][paper_key]
        log_download(call.from_user.id, f"{sub_key}_{paper['year']}")
        bot.answer_callback_query(call.id, "Sending PDF...")
        try:
            bot.send_document(
                call.message.chat.id,
                paper["id"],
                caption=f"{subject['emoji']} {subject['name']} - {paper['year']}\n\n✅ From 𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰"
            )
        except Exception as e:
            bot.answer_callback_query(call.id, "❌ Error sending file. Check File ID.", show_alert=True)

    elif call.data == "stats_total":
        stats = load_stats()
        text = f"📊 *Bot Statistics*\n\n"
        text += f"👥 Total Users: {stats['total_users']}\n"
        text += f"⬇️ Total Downloads: {stats['total_downloads']}\n\n"
        for sub_key, sub_data in SUBJECTS.items():
            text += f"{sub_data['emoji']} {sub_data['name']}: {len(sub_data['papers'])} papers\n"
        bot.answer_callback_query(call.id, text, show_alert=True)

    elif call.data == "admin_stats" and call.from_user.id == ADMIN_ID:
        stats = load_stats()
        text = f"📈 *Admin Statistics*\n\n"
        text += f"👥 Total Users: {stats['total_users']}\n"
        text += f"⬇️ Total Downloads: {stats['total_downloads']}\n\n"
        text += f"*Top 5 Papers:*\n"
        top_papers = sorted(stats["downloads"].items(), key=lambda x: x[1], reverse=True)[:5]
        for paper, count in top_papers:
            text += f"• {paper}: {count} downloads\n"
        text += f"\n*Recent Users:*\n"
        recent = list(stats["users"].items())[-5:]
        for uid, data in recent:
            text += f"• {data['username']}: {data['downloads']} downloads\n"
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id == ADMIN_ID:
        stats = load_stats()
        text = f"📈 *Admin Statistics*\n\n👥 Users: {stats['total_users']}\n⬇️ Downloads: {stats['total_downloads']}"
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Admin only command")

print("🤖 Bot Started...")
bot.infinity_polling()
