from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os
import re

TOKEN = os.environ["BOT_TOKEN"]

# --- Экранирование спецсимволов для MarkdownV2 ---
def escape(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(f"\\{c}" if c in escape_chars else c for c in text)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

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
        "/убаюкать": "убаюкала",
        "/нагнуть": "поставила раком",
        "/отшлепать": "отшлёпала",
        "/отсосать": "отсосала",
        "/связать": "связала",
        "/отмудохать": "отмудохала",
        "/отпиздить": "отпиздила",
        "/срач": "устроила срач с",
        "/мет": "дала пакетик метамфетамина",
        "/меф": "дала пакетик мефедрона",
        "/кокс": "дала пакетик кокаина",
        "/герыч": "дала пакетик героина",
        "/пожамкать": "пожамкала",
        "/сися": "помацала за сисю",
        "/попа": "помяла жопу",
        "/фистинг": "запихнула руку по самый локоть в жопу",
        "/воскресить": "воскресила",
        "/обоссать": "обоссала",
        "/обосрать": "обосрала",
        "/понюхать": "понюхала",
    }
    
    self_actions = {
        "/умереть": "внезапно умерла",
        "/суицид": "совершила суицид",
        "/заснуть": "уснула",
        "/улететь": "улетела в космос",
        "/окно": "вышла в окно",
        "/кончить": "кончила",
        "/зига": "плотно потянулась к солнцу",
    }

    text = update.message.text.strip()
    command = text.split()[0]

     # Кликабельное имя отправителя
    sender_name = escape(update.effective_user.first_name)
    sender = f"[{sender_name}](tg://user?id={update.effective_user.id})"

    
    # Само-действия
    if command in self_actions:
        action_text = self_actions[command]
        await update.message.reply_text(
            f"{sender} {action_text}",
            parse_mode="MarkdownV2"
        )
        return
    
 # --- Действия с целью ---
    if command in actions:
        action_verb = actions[command]

        # 1. Ищем @username
        mentioned_users = re.findall(r'@[\w\d_]+', text)
        if mentioned_users:
            target = mentioned_users[0]  # Telegram сам сделает кликабельным
        elif update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user
            target_name = escape(target_user.first_name)
            target = f"[{target_name}](tg://user?id={target_user.id})"
        elif len(text.split()) > 1:
            target = escape(" ".join(text.split()[1:]))
        else:
            target = "всех 🫂"

        await update.message.reply_text(
            f"{sender} {action_verb} {target}",
            parse_mode="MarkdownV2"
        )


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
