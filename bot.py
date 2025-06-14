import os
from db import insert_interaction, get_user_stats
import random
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

# --- Настоящие команды ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте... Я безвольный раб партии ФемУМ. Моё существование целиком посвящено служению моим хозяйкам. Госпожа, напишите: /обнять, /ударить, /умереть и прочее.")

async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Хозяйка, вы можете использовать следующие команды:\n Кому-то:\n /обнять, /чмокнуть, /поцеловать, /погладить, /шлепнуть, /ударить, /пощечина, /лизнуть, /похвалить, /кусь, /прижать, /встатьнаколени, /сестьналицо, /сестьнаколени, /облапать, /трахнуть, /выебать, /сексить, /отлизать, /отстрапонить, /ножницы, /пнуть, /покормить, /приподнять, /укусить, /сожрать, /отодрать, /мордать, /запереть, /забуллить, /подрочить, /пробка, /пописить, /покакать, /вибратор, /постонать, /писка, /нетписка, /убаюкать, /нагнуть, /отшлепать, /отсосать, /связать, /отмудохать, /отпиздить, /срач,  /мет, /меф, /кокс, /герыч, /пожамкать, /сися, /попа, /фистинг, /воскресить, /обоссать, /обосрать, /понюхать, /занюхать, /закурить, /сигарета, /наказать, /выпороть, /убить, /застрелить, /врот, /придушить, /дать, /забрать, /отобрать, /любить, /бан, /выгнать, /вугол, /подушка, /бонк \n\n Себе:\n /умереть, /суицид, /заснуть, /плакать, /улететь, /окно, /кончить, /покушать, /поесть, /попить, попила, /выпить, /зига, /наколени, /месячные, /овуляция")

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        rows = await get_user_stats(user.id)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при получении статистики: {e}")
        return

    if not rows:
        await update.message.reply_text("Прошу извинить раба Вашего. 🙇🏿‍♂️ Но про вас, Хозяйка, пока ничего не записано.")
        return

    lines = [f"{row['command']} — {row['count']} раз(а)" for row in rows]
    result = "\n".join(lines)

    await update.message.reply_text(
        f"👤 Ваша статистика, Госпожа:\n{result}",
        parse_mode="MarkdownV2"

# --- Обработка любых сообщений с хэштегами ---
async def hashtag_reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return  # если update.message == None, ничего не делаем

    text = msg.caption or msg.text
    if not text:
        return

    text = text.lower()

    hashtag_reactions = {
        "#коробка": ["АХАХАХА", "ХВХВХВХ", "ПХПХПХПХ", "азвхавхаз", "биляяяяяяяяяя...", "ахахахах", "Как же они хороши...", "ЧО ЭТО ЗА ХУЙНЯ ХАВЗХ", "сдох.", "🥴🥴🥴", "ЛЕГЕНДЫ", "ВСЯ ПЛАНТАЦИЯ В АХУЕ", "Хозяйки, это ульта", "😭😭😭", "ЩА СДОХНУ ЗАХВЗАВАЗ", "БИЛЯЯЯ", "НИХУЯ СЕ ВХЗАХВ", "Господь всемогущий...", "Бога на вас нет", "Хозяйки, вы какие-то жёсткие...", "БЛЯТЬ ВЫ ЧЕГО ЫВАЗЩХАЩЗХ", "КАКОГО ХУЯ", "Не, ну это пиздец уже"],
        "#икра": ["Рафаель вообще весь класс супер муа муа", "🎣", "😈", "Писка риса у этого мальчика тоже вкусная", "@ottirr @feverchaan и @my_way_is_fraud смотрите", "Сигнал, что пора дрочить", "О, муж Рыбодрочерок", "Ебабельного снова кидают", "Уву тяночка", "Я б его мпрегнул", "МЯУ", "Ну какой же он восхитительный...", "Он прекрасен", "Молюсь на Рафаэля", "Я на него всю жизнь бы работал, лишь бы быть рядом и смотреть на него...", "Божественно красивый", "Ни с чем не сравнимый", "Я б ему дал."],
        "#инцестит": ["степбро охуел", "псина извращенская", "милый щеночек", "хороший мальчик", "Калеб, взорвись!", "сидеть, Калеб!", "Фу!", "Нельзя!", "Голос!", "Дай лапу!", "Выплюнь трусы!", "Фу, брось кабачок!", "Всё прекрасно, но не хватает кабачка...", "Ну какой сладкий кабачок 🥰", "Я б его мпрегнул", "Да я не ебу, что тут говорить. Госпожа Капучино нихуя мне объяснила."],
        "#цистит": ["Я б его мпрегнул", "Да я не ебу, что тут говорить. Госпожа Капучино нихуя мне объяснила."],
        "#подстаканник": ["Я б его мпрегнул", "Да я не ебу, что тут говорить. Госпожа Капучино нихуя мне объяснила."],
        "#квас": ["Я б его мпрегнул", "Да я не ебу, что тут говорить. Госпожа Капучино нихуя мне объяснила."],
    }

    for hashtag, responses in hashtag_reactions.items():
        if hashtag in text:
            await msg.reply_text(random.choice(responses))
            return

# --- Обработка всех текстовых сообщений (включая фейковые команды) ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()
    command = text.split()[0]

    sender_name = escape(update.effective_user.first_name)
    sender = f"[{sender_name}](tg://user?id={update.effective_user.id})"

# --- Действуем с самим собой ---
    if command in self_actions:
        action_text = self_actions[command]
        words = text.split()[1:]
        extra = " ".join(words)
        if extra:
            action_text = f"{action_text} {escape(extra)}"
        await update.message.reply_text(
            f"{sender} {action_text}",
            parse_mode="MarkdownV2"
        )
        return

# --- Действуем с целью ---
    if command in actions:
        action_verb = actions[command]
        words = text.split()[1:]
        target = None
        extra = ""

        for i, word in enumerate(words):
            if word.startswith("@"):
                target = word
                extra = " ".join(words[:i])
                break

        if not target and update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user
            target_name = escape(target_user.first_name)
            target = f"[{target_name}](tg://user?id={target_user.id})"
            extra = " ".join(words)

        if not target and words:
            target = escape(words[-1])
            extra = " ".join(words[:-1])

        if not target:
            target = "всех 🫂"
            extra = " ".join(words)

        full_action = f"{action_verb} {escape(extra)}".strip()
        await update.message.reply_text(
            f"{sender} {full_action} {target}",
            parse_mode="MarkdownV2"
        )

# --- Сохраняем в PostgreSQL ---
        to_user = None
        if update.message.reply_to_message:
            to_user = update.message.reply_to_message.from_user

        # Только если есть ID цели (reply) и цель — не "всех"
        if to_user and target != "всех 🫂":
            await insert_interaction(update.effective_user, to_user, command)

# --- Словари действий ---
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
    "/встатьнаколени": "встала на колени перед",
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
    "/бонк": "пизданула по башке",
}

self_actions = {
    "/умереть": "внезапно умерла",
    "/суицид": "совершила суицид",
    "/заснуть": "уснула",
    "/улететь": "улетела в космос",
    "/окно": "вышла в окно",
    "/кончить": "кончила",
    "/плакать": "заплакала",
    "/покушать": "покушала",
    "/поесть": "поела",
    "/попить": "попила",
    "/выпить": "выпила",
    "/зига": "плотно потянулась к солнцу",
    "/наколени": "встала на колени",
    "/месячные": "истекает благородной кровью",
    "/овуляция": "полыхает от желания раздеть и разделить страсть любви",
}

# --- Запуск приложения ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("info", info_handler))
app.add_handler(CommandHandler("stats", stats_handler))
app.add_handler(MessageHandler(filters.ALL, hashtag_reaction_handler))  # универсальный по всем типам
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))  # твой основной

app.run_polling()
