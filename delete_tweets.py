# Author: @pdiddysoldnames
# Date: 03/30/2020
# Description: Deletes old tweets that are not important.

import twitter, time, os, csv

# there may be a bug with Twitter's sleep_on_rate_limit parameter.  If you have a ton of tweets
# and you find that the script isn't sleeping correctly, uncomment out line 65 (time.sleep(6)) before
# the recursive return and input your most recent max_id into get_tweets() instead of starting over at 0 (if you want).

"""initialize api keys and access tokens.  Retrieve from twitter via your developer account."""
api_key = ''  # get yer own
api_secret_key = ''  # get yer own
access_token = ''  # get yer own
access_token_secret = ''  # get yer own

"""instantiates API and choose to sleep when request limit is hit"""
api = twitter.Api(consumer_key=api_key, consumer_secret=api_secret_key,
                  access_token_key=access_token, access_token_secret=access_token_secret,
                  sleep_on_rate_limit=True)

"""initialize screen name"""
screen_name = api.VerifyCredentials().screen_name

"""update delete_year to desired year to inspect tweets for deletion from that year going back in time.  
Update delete_fav_count to keep tweets that have that many favs or higher (set to 0 if you'd like to delete all)"""
delete_year = 2019
delete_fav_num = 3

"""creates excel sheet to add deleted tweets to so you won't miss them too much"""
file_path = os.path.dirname(__file__)
csv_path = os.path.join(file_path, 'deleted_tweets_{}andOlder.csv'.format(delete_year))

"""recursively deletes tweets that meet the deletion criteria"""
def get_tweets(max_id):
    tweets = api.GetUserTimeline(screen_name=screen_name, count=200, max_id=max_id)
    old_max_id = max_id

    for tweet in tweets:

        tweet_dict = tweet.AsDict()
        date = tweet_dict.get('created_at')
        fav_count = tweet_dict.get('favorite_count')
        year = date[-4:]
        tweet_text = tweet_dict.get("text")
        max_id = tweet_dict.get('id')

        if int(year) <= delete_year and (fav_count is None or int(fav_count) < delete_fav_num):

            try:
                with open(csv_path, mode='a', encoding="utf-8-sig") as csv_in:
                    writer = csv.writer(csv_in)
                    writer.writerow([tweet_text])

            except Exception as e:
                print(e)
                break

            api.DestroyStatus(tweet_dict.get('id'))

    if old_max_id == max_id:
        print('Complete!')
        return
    else:
        print(max_id)
        # time.sleep(6)
        return get_tweets(max_id)

"""begin looking through tweets beginning with most recent tweet then going back in time"""
if __name__ == "__main__":
    get_tweets(0)
