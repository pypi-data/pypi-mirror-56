# joke APIs pulled from https://www.programmableweb.com/category/humor/api
from .joke_apis import Jokes
import sys


def main():
	jokes = Jokes(sys.argv)
	print(f'\n\n{jokes.tell()}\n\n')


if __name__ == '__main__':
	main()