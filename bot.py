import tweepy
import schedule
import random
from datetime import datetime, timedelta, timezone
from art import Art, get_line_count, get_row
from utilities.utils import get_secrets, authorize_user


class Bot:
    def run_art_tweet(self):
        try:
            index = random.randint(0, self.total_line_count)
            print(f'selecting index: {index} / {self.total_line_count}')
            selected_art = get_row(self.art_file, index)
            while selected_art == None:
                index = random.randint(0, self.total_line_count)
                selected_art = get_row(self.art_file, index)
                print(f'reselecting index: {index} / {self.total_line_count}')
            print(f'{selected_art}')
            self.api.update_status(f'{selected_art}')
            self.last_tweet_time = datetime.now(timezone.utc)
            print(f"BOT SUCCESSFUL ART TWEET AT {self.last_tweet_time}")
        except Exception as e:
           print(f"Error... {e} at {datetime.now(timezone.utc)}")


    def run_retweet(self):
        SEARCH_TERMS = ['Art', 'Painting', 'En Plein Air', 'Alla Prima', "sketch", "drawing", "sculpture"]
        try:
            found_tweets = []
            for term in SEARCH_TERMS:
                found_tweets += self.api.search(term, lang='en',
                                                result_type='recent', count=1000)
            # remove the unneeded things
            found_tweets = [t._json for t in found_tweets]
            # make sure not too old
            found_tweets = [t for t in found_tweets if self.str_to_time(
                t['created_at']) > self.last_retweet_time]
            # make sure they contain a link/image/video
            found_tweets = [t for t in found_tweets if 'http' in t['text']]
            # make sure no retweets
            found_tweets = [t for t in found_tweets if not (
                'retweeted_status' in t)]
            # select most popular one
            tweet = max(found_tweets, key=self.selection_function)

            self.api.retweet(tweet['id'])
            self.last_retweet_time = datetime.now(timezone.utc)
            print(f"BOT SUCCESSFUL RETWEET AT {self.last_retweet_time}")
        except Exception as e:
            print(f"Error... {e} at {datetime.now(timezone.utc)}")

    def __init__(self):
        # Authenticate to Twitter
        self.secrets = get_secrets()
        auth = tweepy.OAuthHandler(self.secrets['consumer key'], self.secrets['consumer secret']) #consumer key, consumer secret
        auth.set_access_token(self.secrets['access key'], self.secrets['access secret']) #access key, secret    
        self.art_file = "MetObjects.csv"
        self.api = tweepy.API(auth)

        self.str_to_time = lambda x: datetime.strptime(
            x, '%a %b %d %H:%M:%S %z %Y')
        self.selection_function = lambda x: int(
            x['favorite_count']) + int(x['retweet_count'])
        self.last_tweet_time = datetime.now(timezone.utc) - timedelta(days=1)
        self.last_retweet_time = datetime.now(timezone.utc) - timedelta(days=1)
        self.total_line_count = get_line_count(self.art_file)
        
        #self.run_art_tweet()
        self.run_retweet()

        schedule.every().day.at("16:00").do(self.run_retweet) #9am PST
        schedule.every().day.at("00:30").do(self.run_art_tweet) #5:30pm PST
        print("successfully booted bot")


if __name__ == '__main__':

    bot = Bot()
    while True:
        schedule.run_pending()