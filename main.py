import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler, CallbackQueryHandler
from telegram.constants import ParseMode
from utils.keyboards import Keyboards, Actions
from utils.AIChatHandler import AIChatHandler
import json
import api.tests as testsApi
import api.take as takeApi
import api.commonProblems as commonProblemsApi
import api.helpingCenters as helpingCentersApi
import utils.auth as authHelper

load_dotenv()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await authHelper.authorization_helper(update, context)
    await update.message.reply_text("Вітаю! Я бот, який допоможе вам пройти психологічні тести.", reply_markup=Keyboards.menuKeyboard) 
    await test_command(update, context)

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    context.user_data['action'] = Actions.TEST

    page_size = 5  
    page_number = context.user_data.get('page_number', 0) 

    tests = testsApi.fetch_tests({'page': page_number, 'pageSize': page_size})

    start_index = page_number * page_size
    end_index = start_index + page_size

    inlineKeyboard = [
        [InlineKeyboardButton(f'{test["title"]}({question_inflection(test["_count"]["questions"])})', callback_data=str(test['id']))]
        for test in tests["content"]
    ]

    # Add navigation buttons
    navigation_buttons = []
    if page_number > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅️", callback_data='prev_page'))
    if end_index < tests['totalElements']:
        navigation_buttons.append(InlineKeyboardButton("➡️", callback_data='next_page'))
    if navigation_buttons:
        inlineKeyboard.append(navigation_buttons)

    reply_markup = InlineKeyboardMarkup(inlineKeyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text("Оберіть тест", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Оберіть тест", reply_markup=reply_markup)



async def select_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    test_id = int(query.data)
    context.user_data['current_test'] = testsApi.fetch_tests_by_id(test_id, context.user_data['auth'])
    await query.delete_message()
    
    await query.message.reply_text(text=f"Ви обрали {context.user_data['current_test']['title']}.\n{context.user_data['current_test']['subtitle']}", parse_mode=ParseMode.MARKDOWN, reply_markup=Keyboards.cancelKeyboard)

    await ask_question(update, context)
    

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_test = context.user_data['current_test']
    context.user_data['action'] = Actions.QUESTION
    
    if 'current_question_index' not in context.user_data:
        context.user_data['current_question_index'] = 0

    question_index = context.user_data['current_question_index']
    
    if question_index >= len(current_test['questions']):
        await finish_test(update, context)
        return
    
    question = current_test['questions'][question_index]
    
    inlineKeyboard = [[
        InlineKeyboardButton(index, callback_data='{' + f'"points":{answer["score"]}, "questionId":{question_index + 1}, "answerId":{answer["id"]}' + '}')
        for index, answer in enumerate(question['answers'], start=1)   
    ]]    
    
    text = f"Запитання {question_index + 1} з {current_test['questions'].__len__()}. {question['title']} \n{question['subtitle'] if 'subtitle' in question else ''}\nОберіть вашу відповідь:"
    for index, answer in enumerate(question['answers'], start=1):
        text += f"\n{index}. {answer['title']}"

    reply_markup = InlineKeyboardMarkup(inlineKeyboard)

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

    data = json.loads(query.data)
    
    points = data['points']
    
    if 'total_points' not in context.user_data:
        context.user_data['total_points'] = 0

    if 'user_answers' not in context.user_data:
        context.user_data['user_answers'] = []

    context.user_data['user_answers'].append({ 'questionId': data['questionId'], 'answerId': data['questionId'] })
    context.user_data['total_points'] += points
    context.user_data['current_question_index'] += 1
    
    await ask_question(update, context)

async def finish_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("Тест завершено. Обробка результатів...")
    total_points = context.user_data['total_points']
    current_test = context.user_data['current_test']
    answers = context.user_data['user_answers']

    takeApi.create_take({'quizId': current_test['id'], 'answers': answers}, context.user_data['auth'])

    await update.callback_query.message.reply_text(f"Ваш результат: {total_points} балів з {current_test['maxScore']}.\n{current_test['summary']}\n\n_Примітка.\nРезультати психологічного тестування надають загальну оцінку вашого стану. Для точної перевірки необхідна особиста консультація зі спеціалістом у сфері психічного здоровʼя_", parse_mode=ParseMode.MARKDOWN, reply_markup=Keyboards.menuKeyboard)
    
    clear_context(context)
    

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    try:
        await update.get_bot().edit_message_reply_markup(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id-1,
            reply_markup=None
        )
    except:
        pass
    await update.message.reply_text("Cкаcовано.", reply_markup=Keyboards.menuKeyboard)

async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    contacts = helpingCentersApi.fetch_centers()
    text = "Контакти безкоштовної психологічної допомоги:\n\n"
    for contact in contacts:
        text += f"{contact['name']} - {contact['workingHours']} \n{contact['phone']}\n\n"
    await update.message.reply_text(text, reply_markup=Keyboards.menuKeyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    context.user_data['action'] = Actions.HELP
    problems = commonProblemsApi.fetch_problems()
    inlineKeyboard = [
        [InlineKeyboardButton(problem['title'], callback_data=problem['id'])]
        for problem in problems
    ]
    inlineKeyboard.append([InlineKeyboardButton('Інше', callback_data='999')])
    reply_markup = InlineKeyboardMarkup(inlineKeyboard)
    await update.message.reply_text("Оберіть, що вас турбує:", reply_markup=reply_markup)

async def select_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    question = ""
    if context.user_data['action'] == Actions.CHAT: 
      question = update.message.text
      # Send an initial message to the user
      message = await update.message.reply_text(text="Генерую відповідь... Це може зайняти до 30 секунд.", parse_mode=ParseMode.MARKDOWN)
      # Initialize the AIChatHandler
      if 'handler' in context.user_data:
          handler = context.user_data['handler']
          handler.context = context
          handler.message = message
          await handler.send_message(question)
          return
    else:
        await query.answer()
        problem_id = int(query.data)
        if problem_id == 999:
            await query.delete_message()
            message = await query.message.reply_text(text=f"Напишіть, що вас турбує, у чат, а штучний інтелект надасть вам відповідь.", reply_markup=Keyboards.cancelKeyboard)
            context.user_data['action'] = Actions.CHAT
            handler = AIChatHandler(context, message)
            context.user_data['handler'] = handler
            
            await handler.start(context.user_data['auth'])
            return
        problem = commonProblemsApi.fetch_problem_by_id(problem_id)
        await query.delete_message()
        await query.message.reply_text(text=f"{problem['description']} [Читати детальніше про самодопомогу в статті]({problem['url']})", parse_mode=ParseMode.MARKDOWN, reply_markup=Keyboards.menuKeyboard)

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await authHelper.authorization_helper(update, context)
    try:
        await update.get_bot().edit_message_reply_markup(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id-1,
            reply_markup=None
        )
    except:
        pass
    if update.message.text == 'Обрати тест':
        await test_command(update, context)
    elif update.message.text == 'Подивитись результати':
        await results_command(update, context)
    elif update.message.text == 'Скасувати':
        await cancel_command(update, context)
    elif update.message.text == 'Що робити, якщо у мене...':
        await help_command(update, context)
    elif update.message.text == 'Психологічна допомога':
        await contacts_command(update, context)
    elif context.user_data.get('action') == Actions.CHAT:
        await select_problem(update, context)
    else:
        await update.message.reply_text('На жаль, я не зрозумів вашу команду.')

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await authHelper.authorization_helper(update, context)
    query = update.callback_query
    await query.answer()
    
    # Handle pagination for test selection
    if query.data == 'prev_page':
        context.user_data['page_number'] = context.user_data.get('page_number', 0) - 1
        await test_command(update, context)
        return
    elif query.data == 'next_page':
        context.user_data['page_number'] = context.user_data.get('page_number', 0) + 1
        await test_command(update, context)
        return

    # Handle pagination for results
    if query.data == 'prev_results_page':
        context.user_data['page_number'] = context.user_data.get('page_number', 0) - 1
        await results_command(update, context)
        return
    elif query.data == 'next_results_page':
        context.user_data['page_number'] = context.user_data.get('page_number', 0) + 1
        await results_command(update, context)
        return

    action = context.user_data.get('action')
    if action == Actions.TEST:
        await select_test(update, context)
    elif action == Actions.QUESTION:
        await answer_question(update, context)
    elif action == Actions.HELP:
        await select_problem(update, context)
    elif action == Actions.RESULTS:
        # Fetch the latest take for the selected quiz
        quiz_id = int(query.data)
        latest_take = takeApi.fetch_latest_take_by_quiz_id(quiz_id, context.user_data['auth'])
        print(latest_take)
        score = 'answers' in latest_take and sum([answer['answer']['score'] for answer in latest_take['answers']]) or 0
        if latest_take:
            result_message = f"Ваш останній результат для тесту \"{latest_take['quiz']['title']}\": {score} балів з {latest_take['quiz']['maxScore']}.\n{latest_take['quiz']['summary']}"
            await query.message.reply_text(result_message, parse_mode=ParseMode.MARKDOWN, reply_markup=Keyboards.menuKeyboard)
        else:
            await query.message.reply_text("Результати для цього тесту не знайдено.", reply_markup=Keyboards.menuKeyboard)

async def results_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_context(context)
    await authHelper.authorization_helper(update, context)
    context.user_data['action'] = Actions.RESULTS

    page_size = 5  
    page_number = context.user_data.get('page_number', 0) 

    quizzes = testsApi.fetch_my_unique_tests(context.user_data['auth'], {'page': page_number, 'pageSize': page_size})

    start_index = page_number * page_size
    end_index = start_index + page_size

    if len(quizzes) == 0:
        await update.message.reply_text("Ви ще не проходили тест.", reply_markup=Keyboards.menuKeyboard)
        return
    inlineKeyboard = [
        [InlineKeyboardButton(quiz['title'], callback_data=str(quiz['id']))]
        for quiz in quizzes['content']
    ]

    # Add navigation buttons
    navigation_buttons = []
    if page_number > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅️", callback_data='prev_results_page'))
    if end_index < quizzes['totalElements']:
        navigation_buttons.append(InlineKeyboardButton("➡️", callback_data='next_results_page'))
    if navigation_buttons:
        inlineKeyboard.append(navigation_buttons)

    reply_markup = InlineKeyboardMarkup(inlineKeyboard)
    
    await update.message.reply_text("Оберіть тест, щоб побачити результати:", reply_markup=reply_markup)

def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def clear_context(context: ContextTypes.DEFAULT_TYPE):
    if 'current_test' in context.user_data:
        del context.user_data['current_test']
    if 'current_question_index' in context.user_data :
        del context.user_data['current_question_index']
    if 'total_points' in context.user_data :
        del context.user_data['total_points']
    if 'user_answers' in context.user_data :
        del context.user_data['user_answers']
    if 'question_message_id' in context.user_data :
        del context.user_data['question_message_id']
    if 'action' in context.user_data :
        del context.user_data['action']
    if 'handler' in context.user_data:
        del context.user_data['handler']
    if 'page_number' in context.user_data:
        del context.user_data['page_number']
    
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
