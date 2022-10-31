import tweepy
import config
from time import sleep
# Your app's API/consumer key and secret can be found under the Consumer Keys
# section of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
consumer_key = config.CONSUMER_KEY
consumer_secret = config.CONSUMER_SECRET

# Your account's (the app owner's account's) access token and secret for your
# app can be found under the Authentication Tokens section of the
# Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
access_token = config.ACCESS_TOKEN
access_token_secret = config.ACCESS_TOEKN_SECRET

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

# If the authentication was successful, this should print the
# screen name / username of the account
print(f"Running Bot user:={api.verify_credentials().screen_name}")

def tweetFollow(user,followList):
    for follwingPerson in followList:
        try:
            status = f"{user} has started following {follwingPerson}"
            api.update_status(status=status)
            sleep(2)
        except Exception as e:
            print(f"Tweet folloing user failed:={e}")


def tweetUnFollow(user, unfollowList):
    for unfollowingPerson in unfollowList:
        try:
            status = f"{user} has unfollowed {unfollowingPerson}"
            api.update_status(status=status)
            sleep(2)
        except Exception as e:
            print(f"Tweet unFollowing user failed:={e}")

def tweetMessage(message):
    try:
        api.update_status(status=message)
        sleep(2)
    except Exception as e:
        print(f"Tweet  failed:={e}")
