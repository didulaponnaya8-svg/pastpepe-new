import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
BOT_USERNAME = "@PastPaperLKBot"

# API 1: Main
API_1 = "https://pastpapers-api.deno.dev/api"
# API 2: Backup
API_2 = "https://api.npkn.net/pastpapers"

logging.basicConfig(level=logging.INFO)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📘 A/L Papers", callback_data='level_al')],
        [InlineKeyboardButton("📗 O/L Papers", callback_data='level_ol')],
        [InlineKeyboardButton("🎲 Random Paper", callback_data='random')],
        [InlineKeyboardButton("✅ Marking Schemes", callback_data='marking_info')]
    ]
    return InlineKeyboardMarkup(keyboard)

def subjects_menu(level):
    al_subs = {'physics': '⚡ Physics', 'chemistry': '🧪 Chemistry', 'biology': '🧬 Biology',
               'combined_maths': '📐 Combined Maths', 'accounting': '💼 Accounting',
               'business_studies': '📊 Business', 'economics': '📈 Economics', 'ict': '💻 ICT'}
    ol_subs = {'mathematics': '📐 Maths', 'science': '🔬 Science', 'english': '📝 English',
               'sinhala': '📖 Sinhala', 'history': '🏛️ History', 'buddhism': '☸️ Buddhism'}

    subjects = al_subs if level == 'al' else ol_subs
    keyboard = []
    items = list(subjects.items())
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i][1], callback_data=f'sub_{level}_{items[i][0]}')]
        if i+1 < len(items):
            row.append(InlineKeyboardButton(items[i+1][1], callback_data=f'sub_{level}_{items[i+1][0]}'))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')])
    return InlineKeyboardMarkup(keyboard)

def years_menu(level, subject):
    years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017']
    keyboard = []
    row = []
    for year in years:
        row.append(InlineKeyboardButton(f"📅 {year}", callback_data=f'get_{level}_{subject}_{year}'))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f'level_{level}')])
    return InlineKeyboardMarkup(keyboard)

async def download_paper(level, subject, year):
    """Try API 1, if fail try API 2"""
    # API 1
    try:
        res = requests.get(f"{API_1}/paper", params={"level": level, "subject": subject, "year": year}, timeout=15).json()
        if res.get('success') and res.get('download_url'):
            return {"success": True, "url": res['download_url'], "size": res.get('size', 'N/A')}
    except:
        pass

    # API 2 Backup
    try:
        res = requests.get(f"{API_2}", params={"level": level, "subject": subject, "year": year}, timeout=15).json()
        if res.get('url'):
            return {"success": True, "url": res['url'], "size": res.get('size', 'N/A')}
    except:
        pass

    return {"success": False}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('logo.png', 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="📚 *PastPaper LK Bot* 📚\n\n"
                        "✅ A/L & O/L Papers 2017-2024\n"
                        "✅ 100% Free PDF Download\n"
                        "✅ Marking Schemes Available\n\n"
                        "👇 Start කරන්න",
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
    except:
        await update.message.reply_text(
            "📚 *PastPaper LK Bot* 📚\n\n✅ A/L & O/L Papers 2017-2024\n\n👇 Start කරන්න",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'main_menu':
        try:
            await query.edit_message_caption("📚 *PastPaper LK Bot* 📚\n\n👇 Subject එකක් තෝරන්න", parse_mode='Markdown', reply_markup=main_menu())
        except:
            await query.edit_message_text("📚 *PastPaper LK Bot* 📚\n\n👇 Subject එකක් තෝරන්න", parse_mode='Markdown', reply_markup=main_menu())

    elif data.startswith('level_'):
        level = data.split('_')[1]
        await query.edit_message_caption(f"📚 *{level.upper()} Subjects*\n\nSubject එකක් තෝරන්න 👇", parse_mode='Markdown', reply_markup=subjects_menu(level))

    elif data.startswith('sub_'):
        parts = data.split('_')
        level = parts[1]
        subject = '_'.join(parts[2:])
        await query.edit_message_caption(f"📅 *{level.upper()} {subject.replace('_', ' ').title()}*\n\nYear එක තෝරන්න 👇", parse_mode='Markdown', reply_markup=years_menu(level, subject))

    elif data.startswith('get_'):
        parts = data.split('_')
        level = parts[1]
        year = parts[-1]
        subject = '_'.join(parts[2:-1])

        msg = await query.message.reply_text("⏳ *Searching PDF...*\n\nPlease wait 5-10 seconds...", parse_mode='Markdown')

        result = await download_paper(level, subject, year)

        if result['success']:
            await query.message.reply_document(
                document=result['url'],
                filename=f"{level.upper()}_{subject}_{year}.pdf",
                caption=f"✅ *{level.upper()} {subject.replace('_', ' ').title()} {year}*\n\n"
                       f"📥 *PDF Downloaded Successfully!*\n"
                       f"📊 Size: {result['size']}\n\n"
                       f"🔸 Marking: `/marking {level} {subject} {year}`\n"
                       f"🔸 New Paper: /start\n\n"
                       f"> {BOT_USERNAME}",
                parse_mode='Markdown'
            )
            await msg.delete()
        else:
            await msg.edit_text(f"❌ *Paper Not Available*\n\n{subject.title()} {year} paper එක දැනට නෑ.\n\nවෙන Year එකක් try කරන්න හෝ /start ගහන්න.")

    elif data == 'random':
        msg = await query.message.reply_text("🎲 *Getting random paper...*", parse_mode='Markdown')
        try:
            res = requests.get(f"{API_1}/random", timeout=15).json()
            if res.get('success') and res.get('download_url'):
                await query.message.reply_document(
                    document=res['download_url'],
                    caption=f"🎲 *Random Paper*\n\n✅ *{res['level'].upper()} {res['subject'].replace('_', ' ').title()} {res['year']}*\n\n> {BOT_USERNAME}",
                    parse_mode='Markdown'
                )
                await msg.delete()
            else:
                await msg.edit_text("❌ Random paper ගන්න බැරි උනා!")
        except:
            await msg.edit_text("❌ Error! Try again later.")

    elif data == 'marking_info':
        await query.answer("Marking Scheme: /marking al physics 2024 වගේ type කරන්න", show_alert=True)

async def paper_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: `/paper al physics 2024`", parse_mode='Markdown')
        return

    level, subject, year = context.args[0].lower(), context.args[1].lower(), context.args[2]
    msg = await update.message.reply_text("⏳ *Downloading PDF...*", parse_mode='Markdown')

    result = await download_paper(level, subject, year)

    if result['success']:
        await update.message.reply_document(
            document=result['url'],
            filename=f"{level.upper()}_{subject}_{year}.pdf",
            caption=f"✅ *{level.upper()} {subject.title()} {year}*\n\n> {BOT_USERNAME}",
            parse_mode='Markdown'
        )
        await msg.delete()
    else:
        await msg.edit_text("❌ Paper එක හම්බුනේ නෑ! /start ගහලා menu එකෙන් බලන්න")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paper", paper_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("PastPaper Bot Started - PDF Mode 🔥")
    app.run_polling()
