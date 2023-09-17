from pymongo import MongoClient
import config

class DataBase:
	def __init__(self):
		cluster = MongoClient(config.MONGO_DB_URL)

		self.db = cluster["Psychological-test-bot"]
		self.users = self.db["Users"]
		self.tests = self.db["Tests"]

		self.tests_count = len(list(self.tests.find({})))
		
	def get_user(self, message):
		user = self.users.find_one({"chat_id": message.chat.id})

		if user is not None:
			return user

		user = {
			"chat_id": message.chat.id,
			"user_id": message.from_user.id,
			"username": message.from_user.username,
            "test_results": []
		}

		self.users.insert_one(user)

		return user
	
	def set_user(self, message, update):
		self.users.update_one({"user_id": message.from_user.id}, {"$set": update})

	def get_test(self, index):
		return self.tests.find_one({"id": index})
	
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