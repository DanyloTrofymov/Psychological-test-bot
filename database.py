from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class DataBase:
	def __init__(self):
		cluster = MongoClient(os.getenv('MONGO_DB_URL'))

		self.db = cluster[os.getenv('MONGO_DB_CLUSTER_NAME')]
		self.users = self.db["Users"]
		self.tests = self.db["Tests"]
		self.results = self.db["Results"]
		self.contacts = self.db["Contacts"]
		self.problems = self.db["Problems"]
		self.requests = self.db["AIRequests"]
		self.tests_count = len(list(self.tests.find({})))
		
	def get_user(self, message):
		user = self.users.find_one({"_id": message.chat.id})

		if user is not None:
			return user
		
		user = {
			"_id": message.chat.id,
            "test_results": []
		}

		self.users.insert_one(user)

		return user
	
	def add_user(self, message):
		if self.users.find_one({"_id": message.chat.id}) is None:
			user = {
				"_id": message.chat.id,
				"test_results": [],
				"sign_up_date": datetime.now().strftime("%Y.%m.%d %H:%M"),
				"last_activity": datetime.now().strftime("%Y.%m.%d %H:%M"),
				}
			self.users.insert_one(user)

	def set_user(self, message, update):
		self.users.update_one({"_id": message.chat.id}, {"$set": update})
	
	def get_all_tests(self):
		return self.tests.find({})
	
	def get_test_by_id(self, _id):
		return self.tests.find_one({"_id": _id})

	def add_test_result(self, message, _id, result, answers):
		test = self.users.find_one({"_id": message.chat.id, "test_results._id": _id})

		if test is None:
			user = self.get_user(message)
			user['test_results'].append({
				"_id": _id,
				"result": result
			})
			self.set_user(message, user)
		else:
			filter = {"_id": message.chat.id, "test_results._id": _id}
			update = {"$set": {"test_results.$.result": result}}
			self.users.update_one(filter, update)
		
		self.results.insert_one({
				"test_id": _id,
				"result": result,
				"date": datetime.now().strftime("%Y.%m.%d %H:%M"),
				"answers": answers,
			})
		

		
	def get_latest_test_results(self, message):
		user = self.get_user(message)
		latest_results = []
		for i in user['test_results']:
			for j in range(1, self.tests_count + 1):
				if i['_id'] == j:
					result = None
					score = i['result']
					test = self.get_test_by_id(j)
					for score_range, outcome in test['result'].items():
						min_score, max_score = map(int, score_range.split('-'))
						if min_score <= score <= max_score:
							result = outcome
							break
					latest_results.append({
						"test_name": test['test_name'],
						"total_points": test['total_points'],
						"score": score,
						"result": result 
						})
					
		return latest_results
	
	def get_all_contacts(self):
		return self.contacts.find({})
	
	def get_all_problems(self):
		return self.problems.find({})
	
	def get_problem_by_id(self, _id):
		return self.problems.find_one({"_id": _id})
	
	def add_AIRequest(self, message, question):
		request = {
			"_id": self.requests.count_documents({}) + 1,
			"request_text": question,
			"date": datetime.now().strftime("%Y.%m.%d %H:%M"),
		}
		user = self.get_user(message)
		self.requests.insert_one(request)

	def set_user_last_activity(self, message):
		user = self.get_user(message)
		if 'last_activity' not in user or user['last_activity'] != datetime.now().strftime("%Y.%m.%d"):
			user['last_activity'] = datetime.now().strftime("%Y.%m.%d")
			self.set_user(message, user)