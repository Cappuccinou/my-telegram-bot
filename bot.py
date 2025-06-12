import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["BOT_TOKEN"]

# --- Экранирование MarkdownV2 спецсимволов ---
def escape(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return ''.join(f"\\{c}" if c in escape_chars else c for c in text)


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
    "/встатьнаколени": "встала на колени перед",
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
    "/постонать": "постонала на ушко",
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
    "/занюхать": "занюхала",
    "/закурить": "закурила",
    "/сигарета": "потушила сигарету об",
    "/наказать": "наказала",
    "/выпороть": "выпорола",
    "/убить": "убила",
    "/застрелить": "застрелила",
    "/врот": "плюнула в рот",
    "/придушить": "придушила",
    "/дать": "дала",
    "/забрать": "забрала",
    "/отобрать": "отобрала",
    "/любить": "любит",
    "/бан": "забанила",
    "/выгнать": "выгнала из чата",
    "/вугол": "поставила в угол",
    "/подушка": "положила подушку под колени",
    }
    
self_actions = {
        "/умереть": "внезапно умерла",
        "/суицид": "совершила суицид",
        "/заснуть": "уснула",
        "/улететь": "улетела в космос",
        "/окно": "вышла в окно",
        "/кончить": "кончила",
        "/покушать": "покушала",
        "/поесть": "поела",
        "/попить": "попила",
        "/выпить": "выпила",
        "/зига": "плотно потянулась к солнцу",
        "/наколени": "встала на колени",
    }



# --- Обработчик /start ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = escape(user.first_name)
    await update.message.reply_text(
        f"Привет, [{name}](tg://user?id={user.id})! 👋\n"
        "Я раб партии ФемУМ, созданный проислуживать своим хозяйкам. Госпожа, используйте команды вроде:\n"
        "`/обнять`, `/поцеловать`, `/ударить`, `/умереть`, и другие.",
        parse_mode="MarkdownV2"
    )


# --- Обработка всех текстовых сообщений ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    command = text.split()[0]

    # Отправитель — кликабельное имя
    sender_name = escape(update.effective_user.first_name)
    sender = f"[{sender_name}](tg://user?id={update.effective_user.id})"

    # --- Само-действия ---
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

    # Убираем команду из текста и разбиваем остальное
    words = text.split()[1:]
    target = None
    extra = ""

    # 1. Ищем @юзера
    for i, word in enumerate(words):
        if word.startswith("@"):
            target = word
            extra = " ".join(words[:i])  # всё до @
            break

    # 2. Если reply
    if not target and update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        target_name = escape(target_user.first_name)
        target = f"[{target_name}](tg://user?id={target_user.id})"
        extra = " ".join(words)

    # 3. Если указали цель просто текстом
    if not target and words:
        target = escape(words[-1])
        extra = " ".join(words[:-1])

    # 4. Никого не указали
    if not target:
        target = "всех 🫂"
        extra = " ".join(words)

    # Сообщение
    full_action = f"{action_verb} {escape(extra)}".strip()
    await update.message.reply_text(
        f"{sender} {full_action} {target}",
        parse_mode="MarkdownV2"
    )


# --- Запуск приложения ---
app = ApplicationBuilder().token(TOKEN).build()
print("Start handler добавлен")
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
