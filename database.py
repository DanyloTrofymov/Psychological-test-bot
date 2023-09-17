from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class DataBase:
	def __init__(self):
		cluster = MongoClient(os.getenv('MONGO_DB_URL'))

		self.db = cluster["Psychological-test-bot"]
		self.users = self.db["Users"]
		self.tests = self.db["Tests"]

		self.tests_count = len(list(self.tests.find({})))
		
	def get_user(self, message):
		user = self.users.find_one({"user_id": message.chat.id})

		if user is not None:
			return user
		
		user = {
			"user_id": message.chat.id,
			"username": message.chat.username,
            "test_results": []
		}

		self.users.insert_one(user)

		return user
	
	def set_user(self, message, update):
		self.users.update_one({"user_id": message.chat.id}, {"$set": update})
	
	def get_all_tests(self):
		return self.tests.find({})
	
	def get_test_by_id(self, test_id):
		return self.tests.find_one({"test_id": test_id})

	def add_test_result(self, message, test_id, result):
		user = self.get_user(message)
		user['test_results'].append({
            "test_id": test_id,
            "result": result
        })

		self.set_user(message, user)
		
	def get_latest_test_results(self, message):
		user = self.get_user(message)
		latest_results = []
		for j in range(1, self.tests_count + 1):
			found = False
			for i in range(user['test_results'].__len__(), 1, -1):
				result = None
				if(user['test_results'][i - 1]['test_id'] == j):
					print(user['test_results'])
					if('test_results' in user):
						score = user['test_results'][i - 1]['result']
						print(score)
						for score_range, outcome in self.get_test_by_id(j)['result'].items():
							min_score, max_score = map(int, score_range.split('-'))
							if min_score <= score <= max_score:
								result = outcome
								break
					found = True
					latest_results.append({
                        "test_name": self.get_test_by_id(j)['test_name'],
                        "result": result 
					})
					break
			if(not found):
				latest_results.append({
                    "test_name": self.get_test_by_id(j)['test_name'],
                    "result": "Ви ще не пройшли цей тест."
                })


		return latest_results
	