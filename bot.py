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
        "/чмокнуть": "чмокнула",
        "/поцеловать": "поцеловала",
        "/погладить": "погладила",
        "/шлепнуть": "шлёпнула",
        "/ударить": "ударила",
        "/пощечина": "дала пощёчину",
        "/лизнуть": "лизнула",
        "/похвалить": "похвалила",
        "/кусь": "кусьнула",
        "/прижать": "прижала к стене",
        "/сестьналицо": "села на лицо",
        "/сестьнаколени": "села на колени",
        "/облапать": "облапала",
        "/трахнуть": "трахнула",
        "/выебать": "выебала",
        "/сексить": "нежно сексит с",
        "/отлизать": "отлизала",
        "/отстрапонить": "отстрапонила",
        "/ножницы": "потёрлась писей с",
        "/пнуть": "пнула",
        "/покормить": "покормила",
        "/приподнять": "приподняла",
        "/укусить": "укусила",
        "/сожрать": "сожрала",
        "/отодрать": "отодрала",
        "/мордать": "морданула",
        "/запереть": "заперла в подвале",
        "/забуллить": "забуллила",
        "/подрочить": "подрочила",
        "/пробка": "вставила пробку в",
        "/пописить": "пописила вместе с",
        "/покакать": "покакала вместе с",
        "/вибратор": "включила дистанционный вибратор",
        "/постонать": "постанала на ушко",
        "/писка": "дала писку риса",
        "/нетписка": "отобрала писку риса",
        "/кончить": "кончила",
        "/убаюкать": "убаюкала",
        "/нагнуть": "поставила раком",
        "/отшлепать": "отшлёпала",
        "/отсосать": "отсосала",
        "/связать": "связать",
        "/отмудохать": "отмудохала",
        "/отпиздить": "отпиздила",
        "/срач": "устроила срач с",
    }
    
    self_actions = {
        "/умереть": "внезапно умерла",
        "/суицид": "совершила суицид",
        "/заснуть": "уснула",
        "/улететь": "улетела в космос",
        "/окно": "вышла в окно",
    }


    # Само-действия
    if text.split()[0] in self_actions:
        action_text = self_actions[text.split()[0]]
        await update.message.reply_text(f"{sender} {action_text}")
        return
    
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

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
