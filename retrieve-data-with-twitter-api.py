######## Retrieve tweets with twitter API v2 ########


import tweepy

from dotenv import load_dotenv
load_dotenv()

import os


## Environment variable pass from .env file
ENV_MY_BEARER_TOKEN = os.getenv("MY_BEARER_TOKEN")

ENV_CONSUMER_KEY = os.getenv("CONSUMER_KEY")
ENV_CONSUMER_SECRET = os.getenv("CONSUMER_SECRET ")

ENV_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ENV_ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


## Authenticate to twitter API with credentials 
client = tweepy.Client(
    bearer_token=ENV_MY_BEARER_TOKEN,
    consumer_key=ENV_CONSUMER_KEY,
    consumer_secret=ENV_CONSUMER_SECRET,
    access_token=ENV_ACCESS_TOKEN,
    access_token_secret=ENV_ACCESS_TOKEN_SECRET
)


search_query = "#covid19 -in:retweets"

# query to search for tweets
query = "#covid19 lang:en -is:retweet"

# Your start and end time for fetching tweets from march 1, 2022 to june 1, 2022
start_time = "2022-03-01T00:00:00Z"
end_time = "2022-06-01T23:59:59Z"


# get tweets from the API 
tweets = client.search_all_tweets(query=query,
                                     start_time=start_time,
                                     end_time=end_time,
                                     tweet_fields = ["created_at", "text", "source"],
                                     user_fields = ["name", "username", "location", "verified", "description"],
                                     max_results = 100,
                                     expansions='author_id'
                                     )

# tweet specific info
print(len(tweets.data))
# user specific info
print(len(tweets.includes["users"]))

# first tweet
first_tweet = tweets.data[0]
dict(first_tweet)


## user information for the first tweet
first_tweet_user = tweets.includes["users"][0]
dict(first_tweet_user)




## import the pandas library
import pandas as pd
# create a list of records
tweet_info_ls = []
# iterate over each tweet and corresponding user details
for tweet, user in zip(tweets.data, tweets.includes['users']):
    tweet_info = {
        'created_at': tweet.created_at,
        'text': tweet.text,
        'source': tweet.source,
        'name': user.name,
        'username': user.username,
        'location': user.location,
        'verified': user.verified,
        'description': user.description
    }
    tweet_info_ls.append(tweet_info)
# create dataframe from the extracted records
tweets_df = pd.DataFrame(tweet_info_ls)
# display the dataframe
tweets_df.head()