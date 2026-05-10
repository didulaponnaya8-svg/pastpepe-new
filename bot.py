import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8105173071:AAGazfT6NIT3VqT6iayapnGpmm9alc9XvVY"
BOT_USERNAME = "@pastdlbbot_bot"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# papers.json file එක load කරනවා
with open('papers.json', 'r', encoding='utf-8') as f:
    PAPERS_DB = json.load(f)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📘 A/L Papers", callback_data='level_al')],
        [InlineKeyboardButton("📗 O/L Papers", callback_data='level_ol')],
        [InlineKeyboardButton("✅ Marking Schemes", callback_data='marking_info')]
    ]
    return InlineKeyboardMarkup(keyboard)

def subjects_menu(level):
    # papers.json එකේ තියෙන subjects විතරක් පෙන්නනවා
    subjects = list(PAPERS_DB.get(level, {}).keys())
    keyboard = []
    row = []
    for sub in subjects:
        row.append(InlineKeyboardButton(f"📚 {sub.replace('_', ' ').title()}", callback_data=f'sub_{level}_{sub}'))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')])
    return InlineKeyboardMarkup(keyboard)

def years_menu(level, subject):
    # papers.json එකේ තියෙන years විතරක් පෙන්නනවා
    years = sorted(PAPERS_DB.get(level, {}).get(subject, {}).keys(), reverse=True)
    keyboard = []
    row = []
    for year in years:
        row.append(InlineKeyboardButton(f"📅 {year}", callback_data=f'get_{level}_{subject}_{year}'))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f'level_{level}')])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"📚 *Welcome {user.first_name}!* 📚\n\n"
        f"🔥 *PastPaper LK Bot* 🔥\n\n"
        f"✅ A/L & O/L Papers 2018-2023\n"
        f"✅ Direct from doenets.lk\n"
        f"✅ 100% Free PDF Download\n\n"
        f"👇 Subject එකක් තෝරන්න",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'main_menu':
        await query.edit_message_text(
            "📚 *PastPaper LK Bot* 📚\n\n👇 Subject එකක් තෝරන්න",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )

    elif data.startswith('level_'):
        level = data.split('_')[1]
        await query.edit_message_text(
            f"📚 *{level.upper()} Subjects*\n\nSubject එකක් තෝරන්න 👇",
            parse_mode='Markdown',
            reply_markup=subjects_menu(level)
        )

    elif data.startswith('sub_'):
        parts = data.split('_')
        level = parts[1]
        subject = '_'.join(parts[2:])
        await query.edit_message_text(
            f"📅 *{level.upper()} {subject.replace('_', ' ').title()}*\n\nYear එක තෝරන්න 👇",
            parse_mode='Markdown',
            reply_markup=years_menu(level, subject)
        )

    elif data.startswith('get_'):
        parts = data.split('_')
        level = parts[1]
        year = parts[-1]
        subject = '_'.join(parts[2:-1])

        url = PAPERS_DB.get(level, {}).get(subject, {}).get(year)

        if url:
            msg = await query.message.reply_text("⏳ *Downloading PDF...*\n\nPlease wait...", parse_mode='Markdown')
            try:
                await query.message.reply_document(
                    document=url,
                    filename=f"{level.upper()}_{subject}_{year}.pdf",
                    caption=f"✅ *{level.upper()} {subject.replace('_', ' ').title()} {year}*\n\n"
                           f"📥 *Download Complete!*\n"
                           f"📡 Source: doenets.lk\n\n"
                           f"> {BOT_USERNAME}",
                    parse_mode='Markdown'
                )
                await msg.delete()
            except Exception as e:
                await msg.edit_text(f"❌ Error downloading PDF: {str(e)}\n\nTry again later.")
        else:
            await query.answer("❌ Paper එක දැනට නැත! Admin update කරනකන් ඉන්න.", show_alert=True)

    elif data == 'marking_info':
        await query.answer("Marking Scheme: /marking al physics 2023 වගේ type කරන්න", show_alert=True)

async def marking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text(
            "❌ *Usage:* `/marking al physics 2023`\n\n"
            "*Example:* `/marking al chemistry 2022`",
            parse_mode='Markdown'
        )
        return

    level, subject, year = context.args[0].lower(), context.args[1].lower(), context.args[2]
    key = f"{level}_{subject}_{year}"
    url = PAPERS_DB.get('marking', {}).get(key)

    if url:
        msg = await update.message.reply_text("⏳ *Downloading Marking Scheme...*", parse_mode='Markdown')
        await update.message.reply_document(
            document=url,
            filename=f"Marking_{key}.pdf",
            caption=f"✅ *Marking Scheme*\n\n{level.upper()} {subject.title()} {year}\n\n> {BOT_USERNAME}",
            parse_mode='Markdown'
        )
        await msg.delete()
    else:
        await update.message.reply_text("❌ Marking scheme එක දැනට නැත!")

if __name__ == '__main__':
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    print("Starting PastPaper LK Bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("marking", marking_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is polling... 100% Online ✅")
    app.run_polling()
