import json

class User:
	_instance = None
	
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance
		
	def __init__(self):
		if not hasattr(self, 'initialized'):
			self.initialized = True
			self.user = {}
			self.get_user()
			
	
	def get_user(self):
		with open("user.json", "r") as f:
			self.user = json.load(f)
		
	def write_user(self):
		with open("user.json", "w") as f:
			json.dump(self.user, f)
		
		
		
		
	def set_user_zipcode(self, zipcode):
		self.user["zipcode"] = zipcode
		self.write_user()
		
	def get_user_zipcode(self):
		self.get_user()
		zipcode = self.user["zipcode"]
		return zipcode
	
	def set_user_wifi_name(self, wifi_name):
		self.user["network_name"] = wifi_name
		self.write_user()

	def get_user_wifi_name(self):
		self.get_user()
		wifi_name = self.user["network_name"] 
		
	def set_user_wifi_password(self, wifi_password):
		self.user["network_password"] = wifi_password
		self.write_user()

	def get_user_wifi_password(self):
		self.get_user()
		wifi_password = self.user["network_password"] 
		
