import json

data = {}

data['api_key'] = input('What is your api key?')
data['api_secret'] = input('What is your api secret?')
data['access_token'] = input('What is your access token?')
data['access_token_secret'] = input('What is your access token secret?')
data['twitter_handle'] = input('What is your Twitter handle?')
data['email'] = input('What is your email?')
data['password'] = input('What is your email password?')
data['name'] = input('What is your name?')

with open('config.json', 'w') as f:
  write(json.dumps(data, sort_keys=True, indent=2))
