from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Инициализация начального баланса
balance = {
    "Долгосрочное": 0,
    "Среднесрочное": 0
}

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Введи начальный баланс:")

# Обработка ввода начального баланса
async def handle_initial_balance(update: Update, context: CallbackContext) -> None:
    try:
        initial_balance = float(update.message.text)
        balance["Долгосрочное"] = initial_balance * 0.5
        balance["Среднесрочное"] = initial_balance * 0.5
        await update.message.reply_text(
            f"Баланс установлен!\n\nДолгосрочное: {balance['Долгосрочное']}\nСреднесрочное: {balance['Среднесрочное']}")
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректное число для баланса.")

# Обработка команды /popolnenie
async def popolnenie(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Выбери тип пополнения: ЗП или Репетство")

# Обработка траты
async def trata(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Введите сумму траты:")

# Обработка баланса
async def balans(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f"Текущий баланс:\n\nДолгосрочное: {balance['Долгосрочное']}\nСреднесрочное: {balance['Среднесрочное']}")

async def handle_income_type(update: Update, context: CallbackContext) -> None:
    if update.message.text.lower() == "зп":
        await update.message.reply_text("Введите сумму ЗП:")
        context.user_data['income_type'] = 'ЗП'
    elif update.message.text.lower() == "репетство":
        await update.message.reply_text("Введите сумму Репетства:")
        context.user_data['income_type'] = 'Репетство'
    else:
        await update.message.reply_text("Неверный выбор. Пожалуйста, выберите ЗП или Репетство.")

async def handle_income_amount(update: Update, context: CallbackContext) -> None:
    try:
        income = float(update.message.text)
        if context.user_data['income_type'] == 'ЗП':
            balance["Долгосрочное"] += income * 0.5
            balance["Среднесрочное"] += income * 0.25
        elif context.user_data['income_type'] == 'Репетство':
            balance["Среднесрочное"] += income * 0.5
        
        await update.message.reply_text(
            f"Пополнение успешно!\n\nДолгосрочное: {balance['Долгосрочное']}\nСреднесрочное: {balance['Среднесрочное']}")
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректную сумму.")

async def handle_expense(update: Update, context: CallbackContext) -> None:
    try:
        expense = float(update.message.text)
        if expense > balance["Среднесрочное"]:
            await update.message.reply_text("Недостаточно средств в разделе 'Среднесрочное'.")
        else:
            balance["Среднесрочное"] -= expense
            await update.message.reply_text(f"Трата учтена!\n\nСреднесрочное: {balance['Среднесрочное']}")
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректную сумму.")

def main() -> None:
    # Вставь сюда свой токен
    application = ApplicationBuilder().token("7719747359:AAHDBYoZNOtg3WC1F-LlpDk7mqtHCdaxm8M").build()

    # Команды бота
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("popolnenie", popolnenie))  # Пополнение
    application.add_handler(CommandHandler("trata", trata))  # Трата
    application.add_handler(CommandHandler("balans", balans))  # Баланс

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_initial_balance))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_income_type))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_income_amount))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_expense))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
