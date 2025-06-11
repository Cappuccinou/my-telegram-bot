from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.environ["BOT_TOKEN"]  # Токен будет добавлен на Render

async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split()[0][1:]
    sender = update.effective_user.first_name

    # Определяем цель
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user.first_name
    elif context.args:
        target = ' '.join(context.args)
    else:
        await update.message.reply_text("Укажи, кого " + command + ", например: /" + command + " @username или ответом на сообщение.")
        return

    actions = {
        "обнять": "обняла",
        "поцеловать": "поцеловала",
        "погладить": "погладила",
        "шлёпнуть": "шлёпнула",
        "ударить": "ударила",
        "лизнуть": "лизнула",
        "похвалить": "похвалила",
        "кусь": "кусьнула",
        "прижать": "прижала",
        "сесть": "села",
        "облапать": "облапала",
        "трахнуть": "трахнула",
        "выебать": "выебала",
        "отлизать": "отлизала",
        "отстрапонить": "отстрапонила",
        "пнуть": "пнула",
        "покормить": "покормила",
        "приподнять": "приподняла",
        "укусить": "укусила",
    }

    action_word = actions.get(command, command)
    response = f"{sender} {action_word} {target}"
    await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()

commands = ["обнять", "поцеловать", "ударить", "погладить", "шлёпнуть", "лизнуть", "похвалить", "кусь", "прижать", "сесть", "облапать", "трахнуть", "выебать", "отлизать", "отстрапонить", "пнуть", "покормить", "приподнять", "укусить"]
for cmd in commands:
    app.add_handler(CommandHandler(cmd, handle_action))

app.run_polling()
