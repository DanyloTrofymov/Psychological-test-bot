import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.getenv('MONGO_DB_URL'))  


db = client["Psychological-test-bot-dev"]
collection = db["Tests"] 

question_id = 0
def set_question_id():
  global question_id
  question_id += 1
  return question_id

document = {
  "_id": collection.count_documents({}) + 1,
  "test_name": "Шкала тривоги Гамільтона (HAM-A/HARS)",
  "questions": [
    {
      "question_id": set_question_id(),
      "question_text": "Тривожний настрій: (стурбованість, очікування найгіршого, тривожні побоювання, дратівливість)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Напруження (відчуття напруження, здригання, плаксивість, тремтіння, відчуття занепокоєння, нездатність розслабитися)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Страхи (темряви, незнайомців, самотності, тварин, натовпу, транспорту)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Інсомнія (утруднене засинання, переривчастий сон, що не приносить відпочинку, почуття розбитості й слабкості при пробудженні, кошмарні сни)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Інтелектуальні порушення (утруднення концентрації уваги, погіршення пам’яті)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Депресивний настрій (втрата звичних інтересів та почуття задоволення від хобі, пригніченість, ранні пробудження, добові коливання настрою)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Соматичний м’язовий біль (біль, посмикування, напруження, судоми клонічні, скрипіння зубами, голос, що зривається, підвищений м’язовий тонус)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Соматичні сенсорні (дзвін у вухах, нечіткість зору, приливи жару і холоду, відчуття слабкості, поколювання)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Серцево-судинні (тахікардія, серцебиття, біль у грудях, пульсація в судинах, часті зітхання)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Респіраторні (тиск і стиснення у грудях, задуха, часті зітхання)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Гастроінтестинальні (утруднене ковтання, метеоризм, біль у животі, печія, відчуття переповненого шлунка, нудота, блювання, бурчання в животі, діарея, запор, зменшення маси тіла)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Сечостатеві (прискорене сечовипускання, сильні позиви на сечовипускання, аменорея, менорагія, фригідність, передчасна еякуляція, втрата лібідо, імпотенція)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Вегетативні (сухість у роті, почервоніння чи блідість шкіри, пітливість, головний біль із відчуттям напруження)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
        {
      "question_id": set_question_id(),
      "question_text": "Поведінка при огляді (совання на стільці, неспокійна жестикуляція і хода, тремор, нахмурювання, напружений вираз обличчя, зітхання чи прискорене дихання, часте ковтання слини)",
      "answers": [
        {"answer_id": 1, "answer_text": "Немає", "points": 0},
        {"answer_id": 2, "answer_text": "Інколи", "points": 1},
        {"answer_id": 3, "answer_text": "Помірно", "points": 2},
        {"answer_id": 4, "answer_text": "Часто", "points": 3},
        {"answer_id": 5, "answer_text": "Дуже часто", "points": 4}
      ]
    },
  ],
  "total_points": 56,
  "result": {
    "0-17": "Лкгуа ступінь тривожності.",
    "18-24": "Ступінь тривожності від легкої до помірної.",
    "25-30": "Ступінь тривожності від помірної до важкої. Рекомендовано звернутися к спеціалісту у сфері психічного здоров’я.",
    "31-56": "Результати вказують на сильне занепокоєння. Рекомендовано звернутися к спеціалісту у сфері психічного здоров’я."
  }
}


insert_result = collection.insert_one(document)


print("Document inserted with ID:", insert_result.inserted_id)

client.close()