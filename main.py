import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler, CallbackQueryHandler
from database import DataBase
load_dotenv()
db = DataBase()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот, який допоможе тобі пройти психологічний тест.")
    await test_command(update, context)

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tests = db.get_all_tests()

    keyboard = [
        [InlineKeyboardButton(test['test_name'], callback_data=str(test['test_id']))]
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
    
    question = current_test['questions'][question_index]
    
    keyboard = [
        [InlineKeyboardButton(answer['answer_text'], callback_data=str(answer['points']))]
        for answer in question['answers']
    ]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    if 'question_message_id' in context.user_data:
        await update.callback_query.edit_message_text(
            text=f"Запитання {question_index + 1}. {question['question_text']} Оберіть вашу відповідь:",
            reply_markup=reply_markup
        )
    else:
        message = await update.callback_query.message.reply_text(
            text=f"Запитання {question_index + 1}. {question['question_text']} Оберіть вашу відповідь:",
            reply_markup=reply_markup
        )
        context.user_data['question_message_id'] = message.message_id

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    
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
    
    db.add_test_result(update.callback_query.message, current_test['test_id'], total_points)
    
    await update.callback_query.message.reply_text(f"Ваш результат: {total_points} балів з {current_test['total_points']}.\n{result}.")
    
    del context.user_data['current_test']
    del context.user_data['current_question_index']
    del context.user_data['total_points']
    

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест сказовано.")
    del context.user_data['current_test']
    del context.user_data['current_question_index']
    del context.user_data['total_points']

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Будь ласка, використовуйте кнопки для відповіді на запитання.')

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(context.user_data.get('current_test') is not None):
        await answer_question(update, context)
    else:
        await select_test(update, context)

async def results_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latest_results = db.get_latest_test_results(update.message)  
    results_message = "Останні результати тестів:\n"
    for result in latest_results:
        if result['result'] is not None:
            results_message += f"{result['test_name']}: {result['score']} балів з {result['total_points']}. {result['result']}\n"
        else:
            results_message += f"{result['test_name']}: Ви ще не пройшли цей тест.\n"

    await update.message.reply_text(results_message)


def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


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




