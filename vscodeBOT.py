from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import nvdlib
from typing import Final
import mysql.connector
from fpdf import FPDF


TOKEN: Final = '6385349407:AAEt4JmsYYkMkjSxkCoTqRw7QGfwRB6BM-4'
BOT_USERNAME: Final = "@botKabbeTbot"
key = "fc1b647f-e97e-477d-bdd5-9df07514ca1f"

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
        await update.message.reply_text("Try writing /cvecpe and name of the cpe you want to check, and you will get the cves.")
        return
    cpe_name = "".join(context.args)
    
    dbcursor.execute("SELECT my_cves FROM cvecpe WHERE id = %s", (cpe_name,))
    result = dbcursor.fetchone()
    if result:
        new_msg = result[0].strip().split("\n")
        new_format = "\n".join(new_msg)
        db_msg = "Retrieved from SQL database."
        await update.message.reply_text(f"CVE ID:\n{new_format}\nCPE Name: {cpe_name}\n{db_msg}")
        return
    r = nvdlib.searchCVE(cpeName=cpe_name, limit = 10, delay=0.6, key = "fc1b647f-e97e-477d-bdd5-9df07514ca1f")
    new_msg = ""
    for eachCVE in r:
        catch = f'{eachCVE.id} {eachCVE.score}\n'
        new_msg += catch

    dbcursor.execute("INSERT INTO cvecpe (id, my_cves) VALUES (%s, %s)", (cpe_name, new_msg))
    connection.commit()

    await update.message.reply_text(f"CVE ID and CVSS:\n{new_msg}\nCPE Name: {cpe_name}\n retrieved from NIST database.")

#selects and returns everything stored in the database.
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dbcursor.execute("SELECT * FROM cvecpe")
    result = dbcursor.fetchall()
    if result:
        responder = ""
        for history in result:
            responder += f"CPE Name: {history[0]}nCVEs\n{history[1]}\n"
        await update.message.reply_text(responder)
        return
    await update.message.reply_text("No history recorded in database.")

"""async def pdf_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Downloadiing PDF...") First try for PDF 
    context.bot.sendDocument(update.effective_chat.id, document=open("bla.pdf", 'rb'))
"""
async def my_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dbcursor.execute("SELECT * FROM cvecpe")
    result = dbcursor.fetchall()
    
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.add_page()
    pdf.set_font('helvetica', '', 16)
    

    if result:
        for recorded in result:
            pdf.cell(0, 10, f"CPE Name: {recorded[0]}")
            pdf.ln()
            cves = recorded[1].split('\n')
            for cve in cves:
                pdf.cell(0, 10, f"{cve}")           
                pdf.ln()
            pdf.cell(0, 10, "---------------------------")
            pdf.ln()
        pdf.output('DB.pdf')

        await context.bot.sendDocument(update.effective_chat.id, document=open("DB.pdf", 'rb'))
        return
    await update.message.reply_text("Database is empty. ^v^")

if __name__ == '__main__':
    #establish connection
    connection = mysql.connector.connect(
        host = "sql11.freemysqlhosting.net",
        user = "sql11688743",
        password = "VtiuLP6LQA",
        database = "sql11688743"
    )

    dbcursor = connection.cursor()

    dbcursor.execute('''
    CREATE TABLE IF NOT EXISTS cvecpe (
        id VARCHAR(255) NOT NULL,  
        my_cves TEXT NOT NULL,
        PRIMARY KEY (id)
        )''')

    print("Bot is starting...")
    my_app = Application.builder().token(TOKEN).build()

    my_app.add_handler(CommandHandler('start', start_command))
    my_app.add_handler(CommandHandler('help', help_command))
    my_app.add_handler(CommandHandler('cvecpe', req_cve))
    my_app.add_handler(CommandHandler('history', history))
    my_app.add_handler(CommandHandler('pdf', my_pdf))
    my_app.add_handler(MessageHandler(filters.TEXT, handle_message))
    my_app.add_error_handler(error)

    print("Polling...")
    my_app.run_polling(poll_interval=3)