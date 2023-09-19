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

    testKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["Скасувати тест"],
        ],
        resize_keyboard=True
    )

class Actions():
    TEST = "test"
    QUESTION = "question"
    HELP = "help"