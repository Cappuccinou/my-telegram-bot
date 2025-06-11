from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ["BOT_TOKEN"]

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    sender = update.effective_user.first_name
    actions = {
        "/обнять": "обняла",
        "/поцеловать": "поцеловала",
        "/погладить": "погладила",
        "/шлёпнуть": "шлёпнула",
        "/ударить": "ударила",
        "/лизнуть": "лизнула",
        "/похвалить": "похвалила",
        "/кусь": "кусьнула",
        "/прижать": "прижала",
        "/сесть": "села",
        "/облапать": "облапала",
        "/трахнуть": "трахнула",
        "/выебать": "выебала",
        "/отлизать": "отлизала",
        "/отстрапонить": "отстрапонила",
        "/пнуть": "пнула",
        "/покормить": "покормила",
        "/приподнять": "приподняла",
        "/укусить": "укусила",
    }

    
    if text.split()[0] in actions:
        action_verb = actions[text.split()[0]]

        # Определяем, на кого была команда
        if update.message.reply_to_message:
            target = update.message.reply_to_message.from_user.first_name
        elif len(text.split()) > 1:
            target = " ".join(text.split()[1:])
        else:
            await update.message.reply_text("Пожалуйста, ответь на сообщение пользователя или укажи его после команды.")
            return
            
        await update.message.reply_text(f"{sender} {action_verb} {target}")
        return

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
