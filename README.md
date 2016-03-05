# twicli

## Description

`twicli` is a basic twitter client for multi-twitter accounts and for use in command-line

## Installation

* Preparation

Assuming you have a fresh Ubuntu installation

	sudo apt-get install python-pip
	sudo pip install twitter

* Clone the repository

Download the client

	git clone https://github.com/bilbopingouin/twicli.git

* Get correct tokens

- After downloading the client, you need to register an application with twitter (API) and write the token into `data/token`.

	Go to https://apps.twitter.com/ click on `create a new app` and follow the instructions.
	You'll be provided with a `Consumer Key (API Key)`. That key should be saved for the client to function.

- Then make authorisation token to connect to your twitter account(s), and save them into `data/oauth/<name>.token`.

	
Additional resources:
	twitter package for python: https://pypi.python.org/pypi/twitter

## Usage

That's it, just run 

	./read_tweets.py --all 

See also

	./read_tweets.py --help
