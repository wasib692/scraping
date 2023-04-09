import csv
import re
from datetime import datetime
import tweepy

consumer_key = ""  # consumer key
consumer_secret = ""  # consumer secret key
access_token_secret = ''  # access token key
access_token = ''  # access token
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def save_csv_file(data):
    print('saving data in csv file...')
    file_name = ''.join(re.findall('\d+', str(datetime.now())))
    path = f'e:/scripts/script3/{file_name}.csv'
    with open(path, 'w', newline='', encoding="utf-8") as csv_file:
        write = csv.writer(csv_file)
        write.writerows(data)


def extract_message(count):
    message_list = []
    try:
        data = api.get_direct_messages(count=count)
        for i in range(len(data)):
            _data = []
            _data.append(data[i]._json['message_create']['message_data']['text'])
            message_list.append(_data)
    except:
        pass
    return message_list


if __name__ == '__main__':
    print('starting...')
    messages = extract_message(count=5000)
    save_csv_file(messages)
    print('finished...')
