import csv
import re
from datetime import datetime
import tweepy

consumer_key = ''  # put consumer key here
consumer_secret = ''  # put consumer secret key here
bearer_token = ''  # put bearer token
access_token_secret = ''  # put access token secret key
access_token = ''  # put access token here
auth = tweepy.OAuth2AppHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def scrape_user_followers(username):
    print('scraping user followers....')
    follower_ids = []
    user_info = []
    for info in tweepy.Cursor(api.get_followers, screen_name=username).pages():
        follower_ids.extend(info)
        print(follower_ids)
        print(len(follower_ids))
        if follower_ids and len(follower_ids) == 600:
            user_info = []
            for data in follower_ids:
                users = dict(accountName=username,
                             userId=data._json['id_str'],
                             fullName=data._json['name'],
                             userName=data._json['screen_name'],
                             followersCount=data._json['followers_count'],
                             followingCount=data._json['friends_count'],
                             isVerified=data._json['verified'],
                             profileLink='http://twitter.com/{}'.format(data._json['screen_name']),
                             dateCreation=data._json['created_at'])
                user_info.append(users)
            save_csv_file(user_info, username)
            follower_ids = []
    if follower_ids and len(follower_ids) != 600:
        for data in follower_ids:
            users = dict(accountName=username,
                         userId=data._json['id_str'],
                         fullName=data._json['name'],
                         userName=data._json['screen_name'],
                         followersCount=data._json['followers_count'],
                         followingCount=data._json['friends_count'],
                         isVerified=data._json['verified'],
                         profileLink='http://twitter.com/{}'.format(data._json['screen_name']),
                         dateCreation=data._json['created_at'])
            user_info.append(users)
    return user_info


def save_csv_file(data, user):
    print('saving data in csv file...')
    file_name = ''.join(re.findall('\d+', str(datetime.now())))
    path = f'e:/scripts/script1/{user}_{file_name}.csv'
    with open(path, 'w', newline='', encoding="utf-8") as csv_file:
        header = ['accountName', 'userId', 'fullName', 'userName', 'followersCount', 'followingCount', 'isVerified',
                  'profileLink', 'dateCreation']
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for i in data:
            writer.writerow(i)


if __name__ == '__main__':
    user_to_scrape = ''  # enter username
    print('starting...')
    if user_to_scrape != '':
        followers = scrape_user_followers(user_to_scrape)
        save_csv_file(followers, user_to_scrape)
        print('finished...')
