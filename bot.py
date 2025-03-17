import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_shop.settings')
import django
django.setup()
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from shop.models import Product

# Загрузка токена из переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")

if not TG_TOKEN:
    raise ValueError("TG_TOKEN не определено. Убедитесь, что переменная окружения TG_TOKEN установлена.")

CURRENCY = "EURO"  # валюта по умолчанию

@sync_to_async
def get_all_products():
    return list(Product.objects.filter(available=True))


@sync_to_async
def get_product_by_id(pid):
    return Product.objects.get(id=pid)


@sync_to_async
def get_cart_summary(cart):
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        s = product.price * qty
        total += s
        items.append(f"{product.name} x{qty} = {s} EURO.")
    return items, total


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton("Корзина", callback_data="show_cart")],
        [InlineKeyboardButton("Личный кабинет", url="http://127.0.0.1:8000/account/")]
    ]
    if update.callback_query:
        # Если вызвали из inline-кнопки, редактируем текущее сообщение
        await update.callback_query.edit_message_text(
            "Добро пожаловать в магазин!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # Если вызвали командой /start (обычное сообщение)
        await update.message.reply_text(
            "Добро пожаловать в магазин!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "catalog":
        products = await get_all_products()
        keyboard = []
        for prod in products:
            keyboard.append([InlineKeyboardButton(f"{prod.name} ({prod.price} EURO.)", callback_data=f"prod_{prod.id}")])
        keyboard.append([InlineKeyboardButton("Главное меню", callback_data="main_menu")])
        await query.edit_message_text("Список товаров:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("prod_"):
        prod_id = int(data.split("_")[1])
        product = await get_product_by_id(prod_id)
        text = f"{product.name}\nЦена: {product.price} EURO.\nОписание: {product.description}"
        keyboard = [
            [InlineKeyboardButton("Добавить в корзину", callback_data=f"add_{prod_id}")],
            [InlineKeyboardButton("Купить на сайте", url="http://127.0.0.1:8000/")],
            [InlineKeyboardButton("Назад к товарам", callback_data="catalog")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("add_"):
        prod_id = int(data.split("_")[1])
        cart = context.user_data.get("cart", {})
        cart[prod_id] = cart.get(prod_id, 0) + 1
        context.user_data["cart"] = cart
        await query.edit_message_text("Товар добавлен в корзину. Нажмите «Корзина» для просмотра или «Главное меню».")

    elif data == "show_cart":
        await show_cart(update, context)

    elif data == "main_menu":
        await start(update, context)


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cart = context.user_data.get("cart", {})
    if not cart:
        await update.callback_query.edit_message_text("Ваша корзина пуста.")
        return
    items, total = await get_cart_summary(cart)
    text = "\n".join(items) + f"\nИтого: {total} EURO."
    keyboard = [
        [InlineKeyboardButton("Главное меню", callback_data="main_menu")],
        [InlineKeyboardButton("Оформить заказ на сайте", url="http://127.0.0.1:8000/checkout/")]
    ]
    await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cart = context.user_data.get("cart", {})
    if not cart:
        await update.message.reply_text("Ваша корзина пуста.")
        return
    context.user_data["cart"] = {}
    await update.message.reply_text("Заказ оформлен (упрощённо).")


def main():
    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(CommandHandler("checkout", checkout))
    app.run_polling()


if __name__ == "__main__":
    main()
