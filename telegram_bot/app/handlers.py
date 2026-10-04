from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from app.database.requests import (
    get_categories,
    get_items_by_category,
    get_item,
    create_order_on_backend
)

router = Router()


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(
        " **Добро пожаловать в ITShop**\n"
        "───────────────────────\n"
        "Узнайте, что возможно с нашими новейшими устройствами.\n\n"
        "Выбирайте лучшее. Оформляйте заказы мгновенно благодаря интеграции с нашей экосистемой.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛍 Перейти к покупкам", callback_data="catalog")]
        ]),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == 'catalog')
async def catalog_handler(callback: CallbackQuery):
    await callback.answer('')
    categories = await get_categories()

    keyboard = []
    for cat in categories:
        # Присваиваем стильные иконки для категорий Apple Store
        icon = "💻"
        if "смарт" in cat.name.lower():
            icon = "📱"
        elif "мон" in cat.name.lower():
            icon = "🖥"
        elif "комп" in cat.name.lower():
            icon = "⚙️"

        keyboard.append([InlineKeyboardButton(text=f"{icon}  {cat.name}", callback_data=f"category_{cat.id}")])

    keyboard.append([InlineKeyboardButton(text="◀️ Главная", callback_data="start")])

    await callback.message.edit_text(
        " **Магазин. Выбирайте лучшее.**\n"
        "───────────────────────\n"
        "Какая категория устройств интересует вас сегодня?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith('category_'))
async def category_handler(callback: CallbackQuery):
    await callback.answer('')
    _, category_name = callback.data.split('_')
    items = await get_items_by_category(category_name)

    keyboard = []
    for item in items:
        # Элегантный список товаров
        keyboard.append(
            [InlineKeyboardButton(text=f"›  {item.title}  |  \${item.price}", callback_data=f"item_{item.id}")])

    keyboard.append([InlineKeyboardButton(text="◀️ Назад к категориям", callback_data="catalog")])

    await callback.message.edit_text(
        f" **{category_name}**\n"
        "───────────────────────\n"
        "Выберите интересующую вас модель для просмотра деталей:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith('item_'))
async def item_handler(callback: CallbackQuery):
    await callback.answer('')
    _, item_id = callback.data.split('_')
    item = await get_item(item_id)

    if not item:
        await callback.message.answer("❌ Продукт временно недоступен.")
        return

    item_category = item.category if hasattr(item, "category") else "Ноутбуки"
    buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍 Оформить заказ", callback_data=f"buy_{item.id}_{item.price}")],
        [InlineKeyboardButton(text=f'◀️ Назад к разделу {item_category}', callback_data=f'category_{item_category}')]
    ])

    # Форматирование характеристик в стиле спецификаций Apple
    spec_text = ""
    if hasattr(item, 'specifications') and item.specifications:
        spec_text = "✦ **Спецификации:**\n"
        for spec_name, spec_val in item.specifications.items():
            spec_text += f" •  _{spec_name}:_  `{spec_val}`\n"
    else:
        spec_text = "✦ **Обзор:**\n" + f"_{item.description or 'Описание готовится к публикации.'}_"

    await callback.message.edit_text(
        f" **{item.title}**\n"
        "───────────────────────\n"
        f"{spec_text}\n"
        "───────────────────────\n"
        f"📍 Наличие в магазине:  `[ Доступно: {item.inventory} шт. ]`\n"
        f"💵 Стоимость:  **\${item.price}**",
        reply_markup=buy_keyboard,
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith('buy_'))
async def buy_item_handler(callback: CallbackQuery):
    await callback.answer('Создаем ваш заказ...')
    _, item_id, price = callback.data.split('_')
    tg_user_id = callback.from_user.id

    # Отправляем заказ в наш Order Service через API Gateway
    success, order_data = await create_order_on_backend(tg_id=tg_user_id, item_id=item_id, price=price)

    if success:
        await callback.message.edit_text(
            " **Благодарим за ваш заказ!**\n"
            "───────────────────────\n"
            "Ваш запрос успешно принят нашей экосистемой и передан на сборку.\n\n"
            f"📦 **Номер заказа:**  `#{order_data.get('id')}`\n"
            f"👤 **ID клиента:**  `{order_data.get('user_id')}`\n"
            f"💵 **Сумма к оплате:**  `${order_data.get('total_price')}`\n"
            f"📊 **Текущий статус:**  `[ {order_data.get('status').upper()} ]`\n"
            "───────────────────────\n"
            "💡 _Информация о вашей покупке мгновенно отправлена через RabbitMQ. Наш сервис уведомлений уже обрабатывает ваш чек._",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏠 На главную", callback_data="start")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            " **Ошибка при оформлении**\n"
            "───────────────────────\n"
            "К сожалению, сейчас невозможно завершить покупку.\n"
            "Пожалуйста, повторите попытку позже или обратитесь в поддержку.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ В каталог", callback_data="catalog")]
            ]),
            parse_mode="Markdown"
        )


@router.callback_query(F.data == 'start')
async def back_to_start(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(
        " **Добро пожаловать в ITShop**\n"
        "───────────────────────\n"
        "Узнайте, что возможно с нашими новейшими устройствами.\n\n"
        "Выбирайте лучшее. Оформляйте заказы мгновенно благодаря интеграции с нашей экосистемой.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛍 Перейти к покупкам", callback_data="catalog")]
        ]),
        parse_mode="Markdown"
    )
