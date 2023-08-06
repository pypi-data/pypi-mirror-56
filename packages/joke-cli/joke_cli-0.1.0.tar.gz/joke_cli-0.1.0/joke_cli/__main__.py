# joke APIs pulled from https://www.programmableweb.com/category/humor/api
import joke_apis
import sys


def main():
	jokes = joke_apis.Jokes(sys.argv)
	print(f'\n\n{jokes.tell()}\n\n')


if __name__ == '__main__':
	main()