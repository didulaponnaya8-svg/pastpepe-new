import os
import requests
import json
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest, Conflict

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
LOGO_FILE = "logo.png"
ADMIN_ID = 8486116629 # << උඹේ Telegram ID එක දාපන්
USERS_FILE = "users.json"

# ============= Channel Settings =============
CHANNEL_USERNAME = "@sl_paperhub" # @ එක්ක Username
CHANNEL_LINK = "https://t.me/sl_paperhub" # Full Link
# ============================================

# ============= STREAMS STRUCTURE =============
STREAMS = {
    "bio_stream": {
        "name": "🧬 Bio Stream", "emoji": "🧬",
        "subjects": {
            "biology": {
                "name": "🧬 Biology", "emoji": "🧬", "years": "2011-2023",
                "papers": {
                    "bio_2023": {"year": "2023", "id": "1dsc1-TXuXySD2Tb26pZafqZLoZUL3DBy"},
                    "bio_2022": {"year": "2022", "id": "1US231ibZFSYwVqEQWmfFXrI2KYumY-S1"},
                    "bio_2021": {"year": "2021", "id": "1U7fnfUZ6wsslU7L7eAxZXXTgEjViKdEm"},
                    "bio_2020": {"year": "2020", "id": "1uyfLx5tIoaEkZuu9-S9iJXkoK1w5YH5u"},
                    "bio_2019": {"year": "2019", "id": "1yWEcJFPxXmHsWqtN-mZWb3vytfq_RWAv"},
                    "bio_2018": {"year": "2018", "id": "1LNL7D8cRJekekfuGCUMkCXoDdBqeqw-g"},
                    "bio_2017": {"year": "2017", "id": "1fCEvtD07JA32TwP_pudB31mptU-MVE3-"},
                    "bio_2016": {"year": "2016", "id": "1qd3D35yz-TglQ_3yJDcqPm7f7Vj8Uxjx"},
                    "bio_2015": {"year": "2015", "id": "1OcaqyWatw1E9AU6gsbhyDOJSUyEnXOFL"},
                    "bio_2014": {"year": "2014", "id": "1tO8s6-fFa9QEoHVF14LDeSWq9CTKV2Vg"},
                    "bio_2013": {"year": "2013", "id": "1-w0U7c_rP_sUzTwNXJjiuCvAoHIc3IJg"},
                    "bio_2012": {"year": "2012", "id": "1Vple1rcjSM_ZCB2hFpHi2g26ZwOmnqFD"},
                    "bio_2011": {"year": "2011", "id": "1m46B0XwT0wILto45xmfJbLVyVO7SotwI"}
                }
            },
            "physics": {
                "name": "⚛️ Physics", "emoji": "⚛️", "years": "2016-2021",
                "papers": {
                    "phy_2021": {"year": "2021", "id": "1ICLaJDoStL3J3wRDmPSJmqihX1tf6ORR"},
                    "phy_2020": {"year": "2020", "id": "1jbpikdzS2tj1Q_X2tOiKYNVPYtZSg-tz"},
                    "phy_2019": {"year": "2019", "id": "1N1I1-HzZdU1_YJ04I5GipyOcpQsn11uF"},
                    "phy_2018": {"year": "2018", "id": "1HWCycDpK82X6ENdrc775BIr3x-CVBAYx"},
                    "phy_2017": {"year": "2017", "id": "14jLO0EA2U4g9O1HX_7bHEjt4cCWgh4LS"},
                    "phy_2016": {"year": "2016", "id": "1yP8OWb5e0ce2dKGV_Yrb95WGozDOXIYY"}
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
                    "chem_2017": {"year": "2017", "id": "14jLO0EA2U4g9O1HX_7bHEjt4cCWgh4LS"},
                    "chem_2016": {"year": "2016", "id": "1XqsC_8__XMv6XhkABCIqBeu2FZk7wMzX"}
                }
            },
            "maths": {
                "name": "📐 Combined Maths", "emoji": "📐", "years": "2012-2023",
                "papers": {
                    "maths_2023": {"year": "2023", "id": "1KnfBXqXDt8XdQgo-fJ23N3dXVYM3iNnS"},
                    "maths_2022": {"year": "2022", "id": "1rV1FfRrLZViSyhdBscYiwU3Z0HRBJGqc"},
                    "maths_2021": {"year": "2021", "id": "1USBVSnWN3HoKz0N_c1j2w7x0xmtA_436"},
                    "maths_2020": {"year": "2020", "id": "1WPASU4XjshbDAcjDN08O452oJ3J3ZdOu"},
                    "maths_2019": {"year": "2019", "id": "1x5X4GOnkM56waRoSjpZW21ijNf62i39v"},
                    "maths_2018": {"year": "2018", "id": "1FH8POD5jAEP1zlMV-Df6d4YiTtwkUR55"},
                    "maths_2017": {"year": "2017", "id": "1DILTRLHAsasTPEeO31_aOvP63xvUA1jD"},
                    "maths_2016": {"year": "2016", "id": "1-Mp8RFORpf1vXw_-547olWS5Ema-NNKO"},
                    "maths_2015": {"year": "2015", "id": "14VFJKE0wPuurBzJnY2_yVYq8st6mCRr7"},
                    "maths_2014": {"year": "2014", "id": "1TuVDuV_WPV8lIdTI1_U_B4e7XVMECv5d"},
                    "maths_2013": {"year": "2013", "id": "19F-Q8jYfIwGXvVO9SCpeTlqN003Syq3A"},
                    "maths_2012": {"year": "2012", "id": "1UwCR0d--pDEGwdiK9hwuIMRnSYpiw-7Z"}
                }
            },
            "agri": {
                "name": "🌾 Agri Science", "emoji": "🌾", "years": "2015-2023",
                "papers": {
                    "agri_2023": {"year": "2023", "id": "PASTE_2023_AGRI_ID"},
                    "agri_2022": {"year": "2022", "id": "PASTE_2022_AGRI_ID"},
                    "agri_2021": {"year": "2021", "id": "PASTE_2021_AGRI_ID"},
                    "agri_2020": {"year": "2020", "id": "PASTE_2020_AGRI_ID"},
                    "agri_2019": {"year": "2019", "id": "PASTE_2019_AGRI_ID"},
                    "agri_2018": {"year": "2018", "id": "PASTE_2018_AGRI_ID"},
                    "agri_2017": {"year": "2017", "id": "PASTE_2017_AGRI_ID"},
                    "agri_2016": {"year": "2016", "id": "PASTE_2016_AGRI_ID"},
                    "agri_2015": {"year": "2015", "id": "PASTE_2015_AGRI_ID"}
                }
            }
        }
    },
    "commerce": {
        "name": "💼 Commerce", "emoji": "💼",
        "subjects": {
            "econ": {"name": "📊 Economics", "emoji": "📊", "years": "2015-2023", "papers": {}},
            "account": {"name": "💰 Accounting", "emoji": "💰", "years": "2015-2023", "papers": {}},
            "business": {"name": "🏢 Business Studies", "emoji": "🏢", "years": "2015-2023", "papers": {}}
        }
    },
    "arts": {
        "name": "🎨 Arts", "emoji": "🎨",
        "subjects": {
            "sinhala": {"name": "📚 Sinhala", "emoji": "📚", "years": "2015-2023", "papers": {}},
            "history": {"name": "🏛️ History", "emoji": "🏛️", "years": "2015-2023", "papers": {}},
            "geography": {"name": "🌍 Geography", "emoji": "🌍", "years": "2015-2023", "papers": {}}
        }
    },
    "tech": {
        "name": "🔧 Technology", "emoji": "🔧",
        "subjects": {
            "et": {"name": "⚙️ ET", "emoji": "⚙️", "years": "2015-2023", "papers": {}},
            "bst": {"name": "🔬 BST", "emoji": "🔬", "years": "2015-2023", "papers": {}},
            "sft": {"name": "💻 SFT", "emoji": "💻", "years": "2015-2023", "papers": {}}
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
    total = 0
    for stream in STREAMS.values():
        for sub in stream["subjects"].values():
            total += len(sub["papers"])
    return total

async def is_user_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except BadRequest:
        return False

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

def join_channel_menu():
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Verify Join", callback_data="verify_join")]
    ]
    return InlineKeyboardMarkup(keyboard)

def main_menu():
    keyboard = []
    for stream_key, stream_data in STREAMS.items():
        btn = InlineKeyboardButton(f"{stream_data['emoji']} {stream_data['name']}", callback_data=f"stream_{stream_key}")
        keyboard.append([btn])
    keyboard.append([InlineKeyboardButton(f"📊 Total Papers: {get_total_papers()}", callback_data="stats")])
    return InlineKeyboardMarkup(keyboard)

def stream_menu(stream_key):
    keyboard = []
    subjects = STREAMS[stream_key]["subjects"]
    row = []
    for sub_key, sub_data in subjects.items():
        count = len(sub_data["papers"])
        btn = InlineKeyboardButton(f"{sub_data['emoji']} {sub_data['name']} ({count})", callback_data=f"sub_{stream_key}_{sub_key}")
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def papers_menu(stream_key, subject_key):
    keyboard = []
    papers = STREAMS[stream_key]["subjects"][subject_key]["papers"]
    if not papers:
        keyboard.append([InlineKeyboardButton("⚠️ No Papers Added Yet", callback_data="noop")])
    else:
        sorted_papers = dict(sorted(papers.items(), reverse=True))
        row = []
        for paper_key, paper_data in sorted_papers.items():
            btn = InlineKeyboardButton(f"📘 {paper_data['year']}", callback_data=f"paper_{stream_key}_{subject_key}_{paper_key}")
            row.append(btn)
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back to Stream", callback_data=f"stream_{stream_key}")])
    return InlineKeyboardMarkup(keyboard)

async def send_new_message(chat_id, context, text, reply_markup, photo=False):
    """Delete old message and send new one - Fix for Logo edit error"""
    if photo:
        try:
            with open(LOGO_FILE, 'rb') as pic:
                await context.bot.send_photo(chat_id=chat_id, photo=pic, caption=text, reply_markup=reply_markup)
        except FileNotFoundError:
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"Start from {user_id}")

    if not await is_user_joined(user_id, context):
        caption = f"""
🔒 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐧𝐞𝐥 𝐅𝐢𝐫𝐬𝐭
━━━━━━━━━━━━━━━━━━━━
📢 Bot එක Use කරන්න අපේ Channel එකට Join වෙන්න

1️⃣ Join Channel Button එක Click කරන්න
2️⃣ Channel එකට Join වෙන්න: {CHANNEL_USERNAME}
3️⃣ Verify Join Button එක Click කරන්න

━━━━━━━━━━━━━━━━━━━━
𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰
        """
        await send_new_message(update.effective_chat.id, context, caption, join_channel_menu(), photo=True)
        return

    save_user(user_id)
    caption = """
🌟 𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰 🌟
━━━━━━━━━━━━━━━━━━━━
🧬 Bio Stream | 💼 Commerce | 🎨 Arts | 🔧 Tech
📚 A/L Past Papers Sinhala Medium
━━━━━━━━━━━━━━━━━━━━
👇 Select Stream Below
    """
    await send_new_message(update.effective_chat.id, context, caption, main_menu(), photo=True)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id!= ADMIN_ID:
        await update.message.reply_text("❌ Admin Only Command")
        return
    if not context.args:
        await update.message.reply_text("📢 Usage:\n/broadcast Your Message Here")
        return
    message = " ".join(context.args)
    users = load_users()
    await update.message.reply_text(f"📤 Broadcasting to {len(users)} users...")
    success = 0
    failed = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 Announcement\n━━━━━━━━━━━━━━━━━━━━\n{message}\n━━━━━━━━━━━━━━━━━━━━\n_𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰_")
            success += 1
        except:
            failed += 1
    await update.message.reply_text(f"✅ Broadcast Complete\n━━━━━━━━━━━━━━━━━━━━\n📤 Sent: {success}\n❌ Failed: {failed}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    logging.info(f"Button: {data} by {user_id}")

    if data == "noop":
        return

    if data == "verify_join":
        if await is_user_joined(user_id, context):
            save_user(user_id)
            text = """
✅ 𝐕𝐞𝐫𝐢𝐟𝐢𝐞𝐝 𝐒𝐮𝐜𝐞𝐬𝐟𝐮𝐥𝐲!
━━━━━━━━━━━━━━━━━━━━
🌟 𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰 🌟
━━━━━━━━━━━━━━━━━━━━
🧬 Bio Stream | 💼 Commerce | 🎨 Arts | 🔧 Tech
📚 A/L Past Papers Sinhala Medium
━━━━━━━━━━━━━━━━━━━━
👇 Select Stream Below
            """
            try:
                await query.message.delete()
            except:
                pass
            await send_new_message(chat_id, context, text, main_menu(), photo=True)
        else:
            await query.answer(f"❌ You haven't joined {CHANNEL_USERNAME} yet!", show_alert=True)
        return

    if not await is_user_joined(user_id, context):
        text = f"🔒 Please join {CHANNEL_USERNAME} first to use the bot!"
        try:
            await query.message.delete()
        except:
            pass
        await send_new_message(chat_id, context, text, join_channel_menu(), photo=True)
        return

    if data == "main_menu":
        text = """
🌟 𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰 🌟
━━━━━━━━━━━━━━━━━━━━
🧬 Bio Stream | 💼 Commerce | 🎨 Arts | 🔧 Tech
📚 A/L Past Papers Sinhala Medium
━━━━━━━━━━━━━━━━━━━━
👇 Select Stream Below
        """
        try:
            await query.message.delete()
        except:
            pass
        await send_new_message(chat_id, context, text, main_menu(), photo=True)
        return

    if data == "stats":
        stats = "📊 Bot Statistics\n━━━━━━━━━━━━━━━━━━━━\n"
        for stream_data in STREAMS.values():
            total = sum(len(s["papers"]) for s in stream_data["subjects"].values())
            stats += f"{stream_data['emoji']} {stream_data['name']}: {total} Papers\n"
        stats += f"━━━━━━━━━━━━━━━━━━━━\n🎯 Total: {get_total_papers()} Papers\n👥 Users: {len(load_users())}"
        await query.answer(stats, show_alert=True)
        return

    if data.startswith("stream_"):
        stream_key = data.replace("stream_", "", 1)
        stream = STREAMS[stream_key]
        text = f"""
{stream['emoji']} {stream['name']}
━━━━━━━━━━━━━━━━━━━━
👇 Select Subject Below
        """
        try:
            await query.message.delete()
        except:
            pass
        await send_new_message(chat_id, context, text, stream_menu(stream_key))
        return

    if data.startswith("sub_"):
        parts = data.split("_", 2)
        stream_key = parts[1]
        subject_key = parts[2]
        logging.info(f"Subject: {stream_key} -> {subject_key}")
        sub = STREAMS[stream_key]["subjects"][subject_key]
        text = f"""
{sub['emoji']} {sub['name']} Past Papers
━━━━━━━━━━━━━━━━━━━━
📅 Years: {sub['years']}
📚 Total: {len(sub['papers'])} Papers
━━━━━━━━━━━━━━━━━━━━
👇 Select Year Below
        """
        try:
            await query.message.delete()
        except:
            pass
        await send_new_message(chat_id, context, text, papers_menu(stream_key, subject_key))
        return

    if data.startswith("paper_"):
        parts = data.split("_", 3)
        stream_key = parts[1]
        subject_key = parts[2]
        paper_key = parts[3]
        paper = STREAMS[stream_key]["subjects"][subject_key]["papers"][paper_key]
        sub = STREAMS[stream_key]["subjects"][subject_key]

        if "PASTE_" in paper['id']:
            await query.message.reply_text(f"⚠️ {sub['name']} {paper['year']} Paper එක තාම Add කරලා නෑ මචං")
            return

        msg = await query.message.reply_text(f"⏳ Downloading...\n{sub['emoji']} {sub['name']} {paper['year']}")
        try:
            r = download_gdrive(paper['id'])
            r.raise_for_status()
            size_bytes = int(r.headers.get('Content-Length', 0))
            size_mb = size_bytes / 1024 / 1024

            if size_mb > 49:
                await msg.edit_text(
                    f"❌ File Size ලොකුයි: {size_mb:.1f}MB\n\n"
                    f"📄 {sub['name']} {paper['year']}\n\n"
                    f"Telegram Limit: 50MB\n"
                    f"Direct Link: https://drive.google.com/file/d/{paper['id']}/view"
                )
                return

            await msg.edit_text(f"📤 Uploading... {size_mb:.1f}MB\n{sub['emoji']} {sub['name']} {paper['year']}")
            await query.message.reply_document(
                document=r.content,
                filename=f"AL_{sub['name']}_{paper['year']}_Sinhala.pdf",
                caption=f"✅ {sub['emoji']} {sub['name']} {paper['year']} Sinhala\n💾 Size: {size_mb:.1f}MB\n\n_𝐋𝐚𝐧𝐤𝐚 𝐏𝐚𝐩𝐞𝐫 𝐇𝐮𝐛 🇱🇰_"
            )
            await msg.delete()
        except requests.exceptions.RequestException:
            await msg.edit_text(
                f"❌ Download Error\n\n"
                f"📄 {sub['name']} {paper['year']}\n"
                f"🔗 File එක Public කරලා නෑ\n\n"
                f"Share → Anyone with the link → Viewer දාන්න"
            )
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)[:200]}")

async def error_handler(update, context):
    logging.error(f"Exception: {context.error}")
    if isinstance(context.error, Conflict):
        logging.error("Conflict detected - Retrying in 10s")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    # Nuclear Fix: Delete webhook before starting
    logging.info("Deleting webhook...")
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook", data={"drop_pending_updates": True})
        time.sleep(2)
        logging.info("Webhook deleted")
    except Exception as e:
        logging.error(f"Webhook delete failed: {e}")

    logging.info("Bot Started - Lanka Paper Hub v11.1 Stream Edition")

    # Retry loop for Conflict
    while True:
        try:
            app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
        except Conflict:
            logging.error("Conflict! Waiting 10s...")
            time.sleep(10)
            continue
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(5)
            continue

if __name__ == '__main__':
    main()
