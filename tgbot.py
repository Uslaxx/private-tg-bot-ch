import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# определение состояний беседы
START, CATEGORY, DESCRIPTION, SAVE = range(4)


# функция обработки команды /start
def start(update, context):
    # выводим приветственное сообщение
    update.message.reply_text("Здравствуйте! Чтобы создать заявку, введите /new")


# функция обработки команды /new
def new_request(update, context):
    # выводим список категорий
    categories = ["Проблема с интернетом", "Проблема с вашим мобильным устройством"]
    keyboard = [categories[i:i + 1] for i in range(0, len(categories), 1)]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Выберите категорию:", reply_markup=reply_markup)
    return CATEGORY


# функция обработки выбора категории
def select_category(update, context):
    # сохраняем выбранную категорию и запрашиваем описание проблемы
    context.user_data['category'] = update.message.text
    update.message.reply_text("Введите описание проблемы:")
    return DESCRIPTION


# функция обработки описания проблемы
def enter_description(update, context):
    # сохраняем описание проблемы и спрашиваем, хотите ли вы сохранить заявку
    context.user_data['description'] = update.message.text
    keyboard = [['Да', 'Нет']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Хотите сохранить заявку?", reply_markup=reply_markup)
    return SAVE


# функция обработки сохранения заявки
def save_request(update, context):
    # если пользователь выбрал "Да", сохраняем заявку
    if update.message.text == "Да":
        # сохраняем заявку в базе данных или файле
        # здесь можно использовать любую удобную вам технологию хранения данных
        category = context.user_data['category']
        description = context.user_data['description']
        update.message.reply_text("Заявка сохранена.")
    else:
        update.message.reply_text("Заявка не сохранена.")
    return ConversationHandler.END


# функция обработки
def cancel(update, context):
    update.message.reply_text("Отмена.")
    return ConversationHandler.END


def main():
    # создаем объект бота и получаем токен
    updater = Updater("TOKEN", use_context=True)
    # создаем объект диспетчера для обработки запросов бота
    dp = updater.dispatcher

    # создаем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("new", new_request))

    # создаем обработчик для состояний беседы
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', new_request)],
        states={
            CATEGORY: [MessageHandler(Filters.text, select_category)],
            DESCRIPTION: [MessageHandler(Filters.text, enter_description)],
            SAVE: [MessageHandler(Filters.text, save_request)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    # запускаем бота
    updater.start_polling()
    updater.idle()


if name == 'main':
    main()
