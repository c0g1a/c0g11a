import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Токен твоего бота
BOT_TOKEN = "8205601722:AAHrPL7aUTX2CMaz3qUwpRsu9YjGQp65dy0"

# ID админа (куда будут приходить заказы)
# Узнай свой ID через @userinfobot или оставь username
ADMIN_ID = "@FastVape_m"  # или числовой ID, например: 123456789

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Главное меню
def get_main_keyboard():
    kb = [
        [KeyboardButton(text="🛒 Сделать заказ")],
        [KeyboardButton(text="📦 Мои заказы")],
        [KeyboardButton(text="❓ FAQ")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Старт
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Добро пожаловать в <b>FastVape</b>!\n\n"
        "Здесь ты можешь заказать премиальные жидкости для вейпов.\n\n"
        "Выбери действие в меню 👇",
        reply_markup=get_main_keyboard()
    )

# Обработка кнопки "Сделать заказ"
@dp.message(F.text == "🛒 Сделать заказ")
async def make_order(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🫐 Midnight Berry - 1290₽", callback_data="order_midnight_berry")
    keyboard.button(text="🥭 Tropical Storm - 1290₽", callback_data="order_tropical_storm")
    keyboard.button(text="🍃 Mint Glacier - 1290₽", callback_data="order_mint_glacier")
    keyboard.button(text="🍦 Vanilla Noir - 1290₽", callback_data="order_vanilla_noir")
    keyboard.adjust(1)
    
    await message.answer(
        " <b>Выберите товар:</b>\n\n"
        "Нажмите на нужный вкус:",
        reply_markup=keyboard.as_markup()
    )

# Обработка выбора товара
@dp.callback_query(F.data.startswith("order_"))
async def process_order_selection(callback: types.CallbackQuery):
    product_map = {
        "order_midnight_berry": "🫐 Midnight Berry",
        "order_tropical_storm": "🥭 Tropical Storm",
        "order_mint_glacier": "🍃 Mint Glacier",
        "order_vanilla_noir": "🍦 Vanilla Noir"
    }
    
    product = product_map.get(callback.data, "Неизвестный товар")
    
    # Сохраняем товар в состоянии (для простоты)
    await callback.message.answer(
        f"✅ Вы выбрали: <b>{product}</b>\n\n"
        "Теперь напишите:\n"
        "1. Ваше имя\n"
        "2. Контакт для связи (Telegram или телефон)\n"
        "3. Количество\n\n"
        "Пример:\n"
        "<i>Иван, @ivanov, 2 шт.</i>"
    )
    
    await callback.answer()

# Обработка текста заказа
@dp.message()
async def process_order_text(message: types.Message):
    # Отправляем заказ админу
    order_text = f"""
🛒 <b>НОВЫЙ ЗАКАЗ</b>

👤 <b>Клиент:</b> {message.from_user.first_name} @{message.from_user.username or 'без username'}
 <b>ID:</b> <code>{message.from_user.id}</code>
📝 <b>Заказ:</b> {message.text}

⏰ <b>Время:</b> {message.date.strftime('%d.%m.%Y %H:%M')}
    """
    
    try:
        await bot.send_message(ADMIN_ID, order_text)
        await message.answer(
            "✅ <b>Заказ отправлен!</b>\n\n"
            "Мы свяжемся с вами в ближайшее время для подтверждения.\n\n"
            "Спасибо за заказ! 🙏"
        )
    except Exception as e:
        await message.answer(
            "⚠️ Произошла ошибка при отправке заказа.\n"
            "Пожалуйста, напишите нам напрямую: @FastVape_m"
        )
        logging.error(f"Error sending order: {e}")

# FAQ
@dp.message(F.text == "❓ FAQ")
async def faq(message: types.Message):
    faq_text = """
❓ <b>Частые вопросы</b>

<b>Как сделать заказ?</b>
Нажмите "🛒 Сделать заказ" и следуйте инструкциям.

<b>Какие способы оплаты?</b>
Карты, электронные кошельки, наличные при получении.

<b>Есть ли скидки?</b>
Да! Скидки по праздникам. Следите за нашим каналом.

<b>Как связаться?</b>
@FastVape_m или https://t.me/Fast_Vape
    """
    await message.answer(faq_text)

# Мои заказы
@dp.message(F.text == "📦 Мои заказы")
async def my_orders(message: types.Message):
    await message.answer(
        "📦 <b>Ваши заказы</b>\n\n"
        "Здесь будет история ваших заказов.\n"
        "Функция в разработке... 🔜"
    )

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())