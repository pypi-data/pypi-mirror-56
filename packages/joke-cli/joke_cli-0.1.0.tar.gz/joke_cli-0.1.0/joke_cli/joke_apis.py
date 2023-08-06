from random import choice
import html
import requests


class Jokes:
	def __init__(self, cmd_args):
		self.args = cmd_args
		self.headers = {
			'Accept': 'application/json',
			'User-Agent': 'joke-cli (drew@drewtadams.com)'
		}
		self.joke_table = {
			'general': [
				self.sameerkumar,
				self.sv443
			],
			'searchable': [
				self.chucknorris,
				self.icanhazdadjoke
			]
		}


	def tell(self):
		''' returns a random, html-escaped joke string '''

		# check if a search term was passed as a command line argument
		if len(self.args) > 1:
			return html.unescape(choice(self.joke_table['searchable'])(self.args[1]))
		else:
			category = choice([k for k,v in self.joke_table.items()])
			return html.unescape(choice(self.joke_table[category])())


	def get_json(self, api_url):
		''' calls the api and returns the response json if the status is 200, otherwise returns False '''
		r = requests.get(api_url, headers=self.headers)
		if r.status_code != 200:
			return False
		else:
			return r.json()


	# -------------------- methods to handle specific json responses -------------------- #
	def chucknorris(self, search=None):
		''' returns a joke string from api.chucknorris.io '''
		jokes_api = f'https://api.chucknorris.io/jokes/search?query={search}' if search else 'https://api.chucknorris.io/jokes/random'
		joke_json = self.get_json(jokes_api)

		if joke_json:
			if 'value' in joke_json:
				return joke_json['value']
			else:
				if joke_json['total'] > 0:
					return choice(joke_json['result'])['value']
				else:
					return 'No jokes turned up with that term. Try again in a minute or try a different term.'
			

	def icanhazdadjoke(self, search=None):
		''' returns a joke string from icanhazdadjoke.com '''
		jokes_api = 'https://icanhazdadjoke.com'

		if search:
			jokes_api += f'/search?term={search}'
		
		joke_json = self.get_json(jokes_api)
		if joke_json:
			if 'joke' in joke_json:
				return joke_json['joke']
			else:
				if joke_json['total_jokes'] > 0:
					return choice(joke_json['results'])['joke']
				else:
					return 'No jokes turned up with that term. Try again in a minute or try a different term.'


	def sameerkumar(self):
		''' returns a joke string from geek-jokes.sameerkumar.website '''
		jokes_api = 'https://geek-jokes.sameerkumar.website/api'
		joke_json = self.get_json(jokes_api)

		if joke_json:
			return joke_json


	def sv443(self):
		''' returns a joke string from sv443.net '''
		jokes_api = 'https://sv443.net/jokeapi/category/Any?blacklistFlags=nsfw,religious,political'
		joke_json = self.get_json(jokes_api)

		if joke_json:
			if joke_json['type'] == 'single':
				return joke_json['joke']
			else:
				return f'{joke_json["setup"]} {joke_json["delivery"]}'
