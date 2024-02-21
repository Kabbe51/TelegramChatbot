import datetime
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import nvdlib
from typing import Final
import myDatabase
import mysql.connector


TOKEN: Final = '6385349407:AAEt4JmsYYkMkjSxkCoTqRw7QGfwRB6BM-4'
BOT_USERNAME: Final = "@botKabbeTbot"
key = "fc1b647f-e97e-477d-bdd5-9df07514ca1f"


dbConfig = {
    "host": "sql11.freemysqlhosting.net",
    "user": "sql11685092",
    "password": "zPDCFSq79C",
    "datbase": "sql11685092"
}

#establish connection
connection = mysql.connector.connect(**dbConfig)

cursor = connection.cursor()

cursor.execute("SHOW TABLES LIKE 'user_requests'")
if not cursor.fetchone():
    cursor.execute("""
        CREATE TABLE user_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            timestamp INT NOT NULL
        )
    """)
    connection.commit()
                   

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to telegram bot.")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, write an existing command to get started. For example /CVE, or /CPE")

async def req(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.message.reply_text("response")

# response handler
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hi, write an existing command to get started."

    if "how are you in?" in processed:
        return "I am bot."

    if "how" in processed:
        return "Please write a command."

    return "I don't understand your command. Please try again."

    if "how" in processed:
        return "Please write a command."

    return "I don't understand your command. Please try again."

# message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id} in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# basic error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused an error {context.error}')


async def req_cve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Try writing /cve and name of the cpe you want to check, and you will get the cves.")
        return
    cpe_name = "".join(context.args)
    r = nvdlib.searchCVE(cpeName=cpe_name, limit = 10)
    for eachCVE in r:
        await update.message.reply_text(f"CVE ID: {eachCVE.id}\nCPE Name: {cpe_name}")

if __name__ == '__main__':
    print("Bot is starting...")
    my_app = Application.builder().token(TOKEN).build()

    my_app.add_handler(CommandHandler('start', start_command))
    my_app.add_handler(CommandHandler('help', help_command))
    my_app.add_handler(CommandHandler('cve', req_cve))
    # msg handler
    my_app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error handler
    my_app.add_error_handler(error)

    print("Polling...")
    my_app.run_polling(poll_interval=3)
