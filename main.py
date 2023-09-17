import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler, CallbackQueryHandler
from telegram.constants import ParseMode
from database import DataBase
load_dotenv()
db = DataBase()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот, який допоможе тобі пройти психологічний тест.")
    await test_command(update, context)

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    tests = db.get_all_tests()

    keyboard = [
        [InlineKeyboardButton(f'{test["test_name"]}({question_inflection(test["questions"].__len__())})', callback_data=str(test['_id']))]
        for test in tests
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Обери тест:", reply_markup=reply_markup)

async def select_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    test_id = int(query.data)
    context.user_data['current_test'] = db.get_test_by_id(test_id)
    
    await query.edit_message_text(text=f"Ви обрали {context.user_data['current_test']['test_name']}. Чудовий вибір!")
    
    await ask_question(update, context)
    

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_test = context.user_data['current_test']
    
    if 'current_question_index' not in context.user_data:
        context.user_data['current_question_index'] = 0
    
    question_index = context.user_data['current_question_index']
    
    if question_index >= len(current_test['questions']):
        await finish_test(update, context)
        return
    
    question = current_test['questions'][question_index]
    
    keyboard = [[
        InlineKeyboardButton(index, callback_data=str(answer['points']))
        for index, answer in enumerate(question['answers'], start=1)   
    ]]    
    
    text = f"Запитання {question_index + 1} з {current_test['questions'].__len__()}. {question['question_text']} Оберіть вашу відповідь:"
    for index, answer in enumerate(question['answers'], start=1):
        text += f"\n{index}. {answer['answer_text']}"

    reply_markup = InlineKeyboardMarkup(keyboard)

    if 'question_message_id' in context.user_data:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    else:
        message = await update.callback_query.message.reply_text(
            text=text,
            reply_markup=reply_markup
        )
        context.user_data['question_message_id'] = message.message_id

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    points = int(query.data)
    
    if 'total_points' not in context.user_data:
        context.user_data['total_points'] = 0
    
    context.user_data['total_points'] += points
    context.user_data['current_question_index'] += 1
    
    await ask_question(update, context)

async def finish_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("Тест завершено. Обробка результатів...")
    total_points = context.user_data['total_points']
    current_test = context.user_data['current_test']
    
    result = None
    for score_range, outcome in current_test['result'].items():
        min_score, max_score = map(int, score_range.split('-'))
        if min_score <= total_points <= max_score:
            result = outcome
            break
    
    db.add_test_result(update.callback_query.message, current_test['_id'], total_points)
    
    await update.callback_query.message.reply_text(f"Ваш результат: {total_points} балів з {current_test['total_points']}.\n{result}.")
    
    clear_context(context)
    

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    await update.message.reply_text("Тест скаcовано.")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Будь ласка, використовуйте кнопки для відповіді на запитання.')

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(context.user_data.get('current_test') is not None):
        await answer_question(update, context)
    else:
        await select_test(update, context)

async def results_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latest_results = db.get_latest_test_results(update.message)  
    if latest_results == []:
        await update.message.reply_text("Ви ще не проходили жодного тесту.")
        return
    results_message = "Останні результати тестів:\n"
    for result in latest_results:
        results_message += f"_{result['test_name']}:_ {result['score']} балів з {result['total_points']}. {result['result']}\n"

    await update.message.reply_text(results_message, parse_mode=ParseMode.MARKDOWN)


def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def clear_context(context: ContextTypes.DEFAULT_TYPE):
    if 'current_test' in context.user_data:
        del context.user_data['current_test']
    if 'current_question_index' in context.user_data :
        del context.user_data['current_question_index']
    if 'total_points' in context.user_data :
        del context.user_data['total_points']
    

def question_inflection(count):
    last_digit = count % 10
    last_two_digits = count % 100

    if last_two_digits in [11, 12, 13, 14]:
        return f"{count} запитань"
    elif last_digit in [1, 2, 3, 4]:
        return f"{count} запитаня"
    else:
        return f"{count} запитань"

def main():
    print('Starting bot')
    app = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('cancel', cancel_command))
    app.add_handler(CommandHandler('test', test_command))
    app.add_handler(CommandHandler('results', results_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_response))

    # Callbacks
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    #Errors
    app.add_error_handler(error)

    print('Polling')
    app.run_polling()

if __name__ == '__main__':
    main()




