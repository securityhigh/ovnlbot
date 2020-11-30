import requests


"""
XenForo API
github.com/securityhigh/xenforo

example:
from xenforo import Api
xf = Api("token")
"""

class Api:
	def __init__(self, url, api_key, api_user=1):
		self.url = url
		self.api_key = api_key
		self.api_user = api_user

		self.headers = {
			'XF-Api-Key': self.api_key,
			'XF-Api-User': str(self.api_user),
			'Content-Type': 'application/x-www-form-urlencoded'
		}


	def find_user(self, username):
		url = self.url + f"/api/users/find-name?username={username}"

		try:
			response = requests.get(url=url, headers=self.headers)
			return response.json()["exact"]

		except:
			return None


	def find_email(self, email):
		url = self.url + f"/api/users/find-email?email={email}"

		try:
			response = requests.get(url=url, headers=self.headers)
			return response.json()["user"]

		except:
			return None


	def users(self, page=1):
		users = {}
		url = self.url + f"/api/users/?page={page}"

		try:
			response = requests.get(url=url, headers=self.headers)

			for item in response.json()["users"]:
				users[item["username"]] = item["user_id"]

		except:
			pass

		return users


	def user(self, username, password, email):
		url = self.url + f"/api/users/?username={username}&password={password}&email={email}"

		try:
			response = requests.post(url=url, headers=self.headers)
			return response.json()["success"]

		except:
			return False


	def avatar(self, username, file):
		files = {'avatar':  open(file, 'rb')}
		url = self.url + f"/api/users/{username}/avatar"

		try:
			response = requests.post(url=url, files=files, headers=self.headers)
			return response.json()["success"]

		except:
			return False


	def thread(self, forum_id, user_id, title, message):
		headers["XF-Api-User"] = str(user_id)
		url = self.url + f"/api/threads/?node_id={forum_id}&title={title}&message={message}"

		try:
			response = requests.post(url=url, headers=self.headers)
			return int(response.json()["thread"]["thread_id"])

		except:
			return 0


	def post(self, thread_id, user_id, message):
		headers["XF-Api-User"] = str(user_id)

		url = self.url + f"/api/posts/?thread_id={thread_id}&message={message}"

		try:
			response = requests.post(url=target, headers=headers)
			return response.json()["success"]

		except:
			return False
