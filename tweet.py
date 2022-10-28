import tweepy

api_key = "..."
api_secrets = "..."
access_token = "..."
access_secret = "..."

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_secrets)
auth.set_access_token(access_token, access_secret)

tweetapi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
