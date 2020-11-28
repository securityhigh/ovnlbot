import requests


"""
XenForo API
github.com/securityhigh/xenforo

example:
from xenforo import Api
xf = Api("token")
"""

class Api:
	def __init__(self, url, api_key):
		self.url = url
		self.api_key = api_key

		self.headers = {
			'XF-Api-Key': self.api_key,
			'XF-Api-User': '1',
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

