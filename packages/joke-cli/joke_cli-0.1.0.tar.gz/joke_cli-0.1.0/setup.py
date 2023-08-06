from setuptools import setup, find_packages


setup(
	name='joke_cli',
	version='0.1.0',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': [ 'joke_cli = joke_cli.__main__:main' ]
	},

	# metadata
    author='Drew Adams',
    author_email='drew@drewtadams.com',
    description='CLI that fetches and prints random jokes',
    keywords=['random', 'jokes'],
    url='https://github.com/drewtadams/joke_apis'
)