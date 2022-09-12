import tweepy

from dotenv import load_dotenv
load_dotenv()

import os


## Environment variable pass from .env file
ENV_MY_BEARER_TOKEN = os.getenv("MY_BEARER_TOKEN")

ENV_CONSUMER_KEY = os.getenv("CONSUMER_KEY")
ENV_CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

ENV_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ENV_ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(ENV_CONSUMER_KEY, ENV_CONSUMER_SECRET)
 
# set access to user's access key and access secret
auth.set_access_token(ENV_ACCESS_TOKEN, ENV_ACCESS_TOKEN_SECRET)


## Authenticate to twitter API with credentials
client = tweepy.Client(
    bearer_token=ENV_MY_BEARER_TOKEN,
    consumer_key=ENV_CONSUMER_KEY,
    consumer_secret=ENV_CONSUMER_SECRET,
    access_token=ENV_ACCESS_TOKEN,
    access_token_secret=ENV_ACCESS_TOKEN_SECRET
)


search_query = "#covid19 -in:retweets has:geo"

# query to search for tweets
query = '#covid19 lang:en -is:retweet (place_country:US "and" (place:Florida OR place:"Panama city" OR place:Tallahassee OR place:Jacksonville))'


# Your start and end time for fetching tweets from march 1, 2022 to june 1, 2022
start_time = "2022-03-01T00:00:00Z"
end_time = "2022-06-01T23:59:59Z"


# get tweets from the API
tweets = client.search_all_tweets(query=query,
                                     start_time=start_time,
                                     end_time=end_time,
                                     tweet_fields = ["created_at", "text", "source","geo"],
                                     user_fields = ["name", "username", "location", "verified", "description"],
                                     max_results = 10, # The `max_results` query parameter value [5000] is not between 10 and 500
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
    api = tweepy.API(auth)
    place = api.geo_id(tweet.geo['place_id'])
    tweet_info = {
        'tweet_id': tweet.id,
        'created_at': tweet.created_at,
        'geo': tweet.geo['place_id'],
        'bounding_box': str(place.bounding_box.coordinates),
        'bb_centroid': str(place.centroid),
        'coordinates': tweet.geo.get('coordinates'),
        'location': user.location,
        #'source': tweet.source,
        #'text': tweet.text,
        #'name': user.name,
        #'username': user.username,
        #'verified': user.verified,
        #'description': user.description
    }
    tweet_info_ls.append(tweet_info)
# create dataframe from the extracted records
tweets_df = pd.DataFrame(tweet_info_ls)

#Remove non Florida tweets
tweets_df = tweets_df[tweets_df['location'].str.contains("Fl|FL|Florida|FLORIDA", na = False)].reset_index(drop=True)

# display the dataframe
tweets_df.head(10)
