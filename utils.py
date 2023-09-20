from telegram import ReplyKeyboardMarkup

class Keyboards():
    menuKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["Обрати тест"],
            ["Подивитись результати"],
            ["Що робити, якщо у мене..."],
            ["Психологічна допомога"]
        ],
        resize_keyboard=True
    )

    cancelKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["Скасувати"],
        ],
        resize_keyboard=True
    )

class Actions():
    TEST = "test"
    QUESTION = "question"
    HELP = "help"
    CHAT = "chat"