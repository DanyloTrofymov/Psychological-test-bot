import pymongo
import config

client = pymongo.MongoClient(config.MONGO_DB_URL)  


db = client["Psychological-test-bot"]
collection = db["Tests"] 


document = {
  "test_id": 1,
  "test_name": "Algebra Test",
  "questions": [
    {
      "question_id": 1,
      "question_text": "Solve for x: 2x + 5 = 12",
      "answers": [
        {"answer_id": 1, "answer_text": "3", "points": 5},
        {"answer_id": 2, "answer_text": "2", "points": 2},
        {"answer_id": 3, "answer_text": "7", "points": 1}
      ]
    },
  ],
  "total_points": 10,
  "result": {
    "0-5": "bad",
    "6-8": "ok",
    "9-10": "great"
  }
}


insert_result = collection.insert_one(document)


print("Document inserted with ID:", insert_result.inserted_id)

client.close()