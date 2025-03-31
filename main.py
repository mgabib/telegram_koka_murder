from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import asyncio
import logging

TOKEN = "7546551355:AAFWib_qIbwH-Dsq0sm-G1Q5SGRyn1LWOr8"
WEBAPP_URL = "https://telegram-webapp-koka-game-murder.onrender.com"  # Замени на свой URL

bot = Bot(token=TOKEN)
dp = Dispatcher()


from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio

TOKEN = "7546551355:AAFWib_qIbwH-Dsq0sm-G1Q5SGRyn1LWOr8"
WEB_APP_URL = "https://telegram-webapp-koka-game-murder.onrender.com"  # Замени на свою ссылку

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Открыть игру", web_app=WebAppInfo(url=WEB_APP_URL)))
    await message.answer("Нажми кнопку, чтобы открыть игру!", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())

# Регистрируем обработчик
dp.message.register(start_handler, Command("start"))


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())

import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Токен бота (замени на свой)
TOKEN = "7546551355:AAFWib_qIbwH-Dsq0sm-G1Q5SGRyn1LWOr8"

# Размеры игрового поля
FIELD_SIZE = 5

# Координаты игрока, маньяка, бонусов и ловушек
player_x, player_y = FIELD_SIZE // 2, FIELD_SIZE // 2
maniac_x, maniac_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
bonus_x, bonus_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
trap_x, trap_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)

# Очки игрока и оружие
score = 0
has_knife = False
has_gun = False

# Кнопки управления
game_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬆️ Вверх")],
        [KeyboardButton(text="⬅️ Влево"), KeyboardButton(text="➡️ Вправо")],
        [KeyboardButton(text="⬇️ Вниз"), KeyboardButton(text="🛒 Магазин")]
    ],
    resize_keyboard=True
)

shop_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔪 Купить нож (10 очков)")],
        [KeyboardButton(text="🔫 Купить пистолет (50 очков)")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

# Функция для отрисовки игрового поля
def draw_field():
    field = [["⬜" for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
    field[player_y][player_x] = "🟢"  # Игрок
    field[maniac_y][maniac_x] = "🔴"  # Маньяк
    field[bonus_y][bonus_x] = "⭐"  # Бонус
    field[trap_y][trap_x] = "⚠️"  # Ловушка
    return "\n".join("".join(row) for row in field)

# Обработчик команды /start
async def start_handler(message: Message):
    global player_x, player_y, maniac_x, maniac_y, bonus_x, bonus_y, trap_x, trap_y, score, has_knife, has_gun
    player_x, player_y = FIELD_SIZE // 2, FIELD_SIZE // 2
    maniac_x, maniac_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
    bonus_x, bonus_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
    trap_x, trap_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)
    score = 0
    has_knife = False
    has_gun = False
    await message.answer("Привет! Беги от маньяка! 🔴 Собирай ⭐ и избегай ⚠️!", reply_markup=game_keyboard)
    await message.answer(draw_field() + f"\n\nОчки: {score}")

# Движение маньяка
def move_maniac():
    global maniac_x, maniac_y

    if maniac_x < player_x:
        maniac_x += 1
    elif maniac_x > player_x:
        maniac_x -= 1

    if maniac_y < player_y:
        maniac_y += 1
    elif maniac_y > player_y:
        maniac_y -= 1

# Движение игрока
async def move_player(message: Message):
    global player_x, player_y, score, bonus_x, bonus_y, trap_x, trap_y, has_knife, has_gun, maniac_x, maniac_y

    if message.text == "⬆️ Вверх" and player_y > 0:
        player_y -= 1
    elif message.text == "⬇️ Вниз" and player_y < FIELD_SIZE - 1:
        player_y += 1
    elif message.text == "⬅️ Влево" and player_x > 0:
        player_x -= 1
    elif message.text == "➡️ Вправо" and player_x < FIELD_SIZE - 1:
        player_x += 1

    # Проверка бонусов и ловушек
    if (player_x, player_y) == (bonus_x, bonus_y):
        score += 5
        bonus_x, bonus_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)

    if (player_x, player_y) == (trap_x, trap_y):
        score -= 3
        trap_x, trap_y = random.randint(0, FIELD_SIZE - 1), random.randint(0, FIELD_SIZE - 1)

    score += 1  # Очки за шаг

    # Двигаем маньяка
    move_maniac()

    # Проверяем, догнал ли маньяк игрока
    if player_x == maniac_x and player_y == maniac_y:
        if has_gun:
            has_gun = False
            await message.answer("🔫 Ты застрелил маньяка! Ты выиграл!", reply_markup=game_keyboard)
        elif has_knife:
            has_knife = False
            await message.answer("🔪 Ты убил маньяка ножом! Ты выиграл!", reply_markup=game_keyboard)
        else:
            await message.answer("😱 Маньяк поймал тебя! Игра окончена.", reply_markup=game_keyboard)
        return

    await message.answer(draw_field() + f"\n\nОчки: {score}")

# Открытие магазина
async def open_shop(message: Message):
    await message.answer("🛒 Добро пожаловать в магазин!", reply_markup=shop_keyboard)

# Покупка ножа
async def buy_knife(message: Message):
    global score, has_knife
    if score >= 10:
        score -= 10
        has_knife = True
        await message.answer("🔪 Ты купил нож! Если маньяк догонит, ты сможешь защититься.", reply_markup=shop_keyboard)
    else:
        await message.answer("❌ Недостаточно очков!", reply_markup=shop_keyboard)

# Покупка пистолета
async def buy_gun(message: Message):
    global score, has_gun
    if score >= 50:
        score -= 50
        has_gun = True
        await message.answer("🔫 Ты купил пистолет! Теперь ты можешь застрелить маньяка.", reply_markup=shop_keyboard)
    else:
        await message.answer("❌ Недостаточно очков!", reply_markup=shop_keyboard)

# Возвращение в игру
async def back_to_game(message: Message):
    await message.answer("Возвращаемся в игру!", reply_markup=game_keyboard)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command("start"))
    dp.message.register(move_player, F.text.in_(["⬆️ Вверх", "⬇️ Вниз", "⬅️ Влево", "➡️ Вправо"]))
    dp.message.register(open_shop, F.text == "🛒 Магазин")
    dp.message.register(buy_knife, F.text == "🔪 Купить нож (10 очков)")
    dp.message.register(buy_gun, F.text == "🔫 Купить пистолет (50 очков)")
    dp.message.register(back_to_game, F.text == "⬅️ Назад")

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

# Клавиатура управления
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("⬆️ Вверх"))
keyboard.add(KeyboardButton("⬅️ Влево"), KeyboardButton("➡️ Вправо"))
keyboard.add(KeyboardButton("⬇️ Вниз"))
keyboard.add(KeyboardButton("🛒 Магазин"))

# Данные об игроках
game_data = {}

@dp.message_handler(commands=["start"])
async def start_game(message: types.Message):
    """Начало игры: выбор сложности."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Легкий"), KeyboardButton("Средний"), KeyboardButton("Тяжелый"))

    await message.answer("Выбери уровень сложности:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["Легкий", "Средний", "Тяжелый"])
async def set_difficulty(message: types.Message):
    """Установка сложности и начало игры."""
    user_id = message.from_user.id
    difficulty = message.text.lower()

    game_data[user_id] = {
        "x": 2, "y": 2,
        "maniac_x": 0, "maniac_y": 0,
        "score": 0, "weapon": None,
        "difficulty": difficulty,
        "turns": 0,
        "bonus_x": None, "bonus_y": None, "bonus_active": False,
        "trap_x": None, "trap_y": None, "trap_active": False
    }

    await message.answer(f"Ты выбрал {difficulty} уровень. Начинай бегать!", reply_markup=keyboard)

def spawn_bonus_or_trap(user_id):
    """Создаёт бонус или ловушку на поле."""
    if user_id not in game_data:
        return

    if random.random() < 0.5:
        game_data[user_id]["bonus_x"], game_data[user_id]["bonus_y"] = random.randint(0, 4), random.randint(0, 4)
        game_data[user_id]["bonus_active"] = True
    else:
        game_data[user_id]["trap_x"], game_data[user_id]["trap_y"] = random.randint(0, 4), random.randint(0, 4)
        game_data[user_id]["trap_active"] = True

@dp.message_handler(lambda message: message.text in ["⬆️ Вверх", "⬇️ Вниз", "⬅️ Влево", "➡️ Вправо"])
async def move_player(message: types.Message):
    """Обработка передвижения игрока и логика игры."""
    user_id = message.from_user.id
    if user_id not in game_data:
        await start_game(message)
        return

    move = {"⬆️ Вверх": (0, -1), "⬇️ Вниз": (0, 1), "⬅️ Влево": (-1, 0), "➡️ Вправо": (1, 0)}
    dx, dy = move[message.text]

    game_data[user_id]["x"] = max(0, min(4, game_data[user_id]["x"] + dx))
    game_data[user_id]["y"] = max(0, min(4, game_data[user_id]["y"] + dy))

    game_data[user_id]["score"] += 1
    game_data[user_id]["turns"] += 1

    # Проверяем бонусы и ловушки
    if game_data[user_id]["bonus_active"] and (game_data[user_id]["x"], game_data[user_id]["y"]) == (game_data[user_id]["bonus_x"], game_data[user_id]["bonus_y"]):
        game_data[user_id]["score"] += 5
        game_data[user_id]["bonus_active"] = False
        await message.answer("🔥 Ты нашел бонус! +5 очков!")

    if game_data[user_id]["trap_active"] and (game_data[user_id]["x"], game_data[user_id]["y"]) == (game_data[user_id]["trap_x"], game_data[user_id]["trap_y"]):
        game_data[user_id]["score"] = max(0, game_data[user_id]["score"] - 3)
        game_data[user_id]["trap_active"] = False
        await message.answer("💀 Ты попал в ловушку! -3 очка!")

    # Движение маньяка в зависимости от сложности
    difficulty = game_data[user_id]["difficulty"]
    if difficulty == "легкий" and game_data[user_id]["turns"] % 2 == 0:
        move_maniac(user_id)
    elif difficulty == "средний":
        move_maniac(user_id)
    elif difficulty == "тяжелый":
        move_maniac(user_id)
        move_maniac(user_id)

    # Проверяем столкновение с маньяком
    if game_data[user_id]["x"] == game_data[user_id]["maniac_x"] and game_data[user_id]["y"] == game_data[user_id]["maniac_y"]:
        if game_data[user_id]["weapon"] == "нож":
            await message.answer("Ты использовал нож и отбился от маньяка!")
            game_data[user_id]["weapon"] = None
        elif game_data[user_id]["weapon"] == "пистолет":
            await message.answer("Ты застрелил маньяка! Победа! 🔥")
            del game_data[user_id]
            return
        else:
            await message.answer("Маньяк поймал тебя! Игра окончена. 😵", reply_markup=ReplyKeyboardRemove())
            del game_data[user_id]
            return

            # Каждые 3 хода появляется новый бонус или ловушка
        if game_data[user_id]["score"] % 3 == 0:
            spawn_bonus_or_trap(user_id)

        await message.answer(f"Очки: {game_data[user_id]['score']}\n"
                             f"Позиция: {game_data[user_id]['x']}, {game_data[user_id]['y']}\n"
                             f"Маньяк: {game_data[user_id]['maniac_x']}, {game_data[user_id]['maniac_y']}")

        def move_maniac(user_id):
            """Маньяк двигается к игроку."""
            if user_id not in game_data:
                return

            player_x, player_y = game_data[user_id]["x"], game_data[user_id]["y"]
            maniac_x, maniac_y = game_data[user_id]["maniac_x"], game_data[user_id]["maniac_y"]

            if maniac_x < player_x:
                maniac_x += 1
            elif maniac_x > player_x:
                maniac_x -= 1

            if maniac_y < player_y:
                maniac_y += 1
            elif maniac_y > player_y:
                maniac_y -= 1

            game_data[user_id]["maniac_x"], game_data[user_id]["maniac_y"] = maniac_x, maniac_y

        if name == "__main__":
            logging.basicConfig(level=logging.INFO)
            executor.start_polling(dp, skip_updates=True)

import asyncio

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Привет, мир!'

if name == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)