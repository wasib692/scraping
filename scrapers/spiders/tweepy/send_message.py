import csv
import tweepy
import os
from csv import DictReader

consumer_key = ''  # put consumer key here
consumer_secret = ''  # put consumer secret key here
bearer_token = ''  # put bearer token
access_token_secret = ''  # put access token secret key
access_token = ''  # put access token here
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

users = []
for i in os.listdir('e:/scripts/script1/followers_data'):
    if i.endswith('.csv'):
        path = 'e:/scripts/script1/followers_data' + '/' + i
        with open(path, 'r', encoding='UTF-8') as f:
            dict_reader = csv.DictReader(f)
            list_of_dict = list(dict_reader)
            for dic in list_of_dict:
                users.append(list(dic.values()))


def send_message(screen_name, text):
    try:
        profile_id = api.get_user(screen_name=screen_name)
        api.send_direct_message(str(profile_id.id), text=text)
        print(f'Message has been sent to {screen_name} successfully!')
    except:
        print(f'{screen_name} is not in your friend list')


if __name__ == '__main__':
    print('starting...')
    for user in users:
        send_message(user[0], user[1])
    print('Finished!!!')
