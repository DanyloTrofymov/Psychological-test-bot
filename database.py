from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class DataBase:
	def __init__(self):
		cluster = MongoClient(os.getenv('MONGO_DB_URL'))

		self.db = cluster[os.getenv('MONGO_DB_CLUSTER_NAME')]
		self.users = self.db["Users"]
		self.tests = self.db["Tests"]
		self.results = self.db["Results"]
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
	
	def set_user(self, message, update):
		self.users.update_one({"_id": message.chat.id}, {"$set": update})
	
	def get_all_tests(self):
		return self.tests.find({})
	
	def get_test_by_id(self, _id):
		return self.tests.find_one({"_id": _id})

	def add_test_result(self, message, _id, result):
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
				"_id": _id,
				"result": result
			})
		

		
	def get_latest_test_results(self, message):
		user = self.get_user(message)
		latest_results = []
		for j in range(1, self.tests_count + 1):
			for i in user['test_results']:
				result = None
				score = i['result']
				for score_range, outcome in self.get_test_by_id(j)['result'].items():
					min_score, max_score = map(int, score_range.split('-'))
					if min_score <= score <= max_score:
						result = outcome
						break
				latest_results.append({
					"test_name": self.get_test_by_id(j)['test_name'],
					"total_points": self.get_test_by_id(j)['total_points'],
					"score": score,
					"result": result 
					})


		return latest_results
	