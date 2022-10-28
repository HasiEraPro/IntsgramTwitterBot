import tweepy

# Your app's API/consumer key and secret can be found under the Consumer Keys
# section of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
consumer_key = "EWkP4LreABvdoPjC6cuQ8cTyq"
consumer_secret = "yQQ5cIr7iGgdRtRFiyj1F4W1VaGKOBLkgPPOPT3BvnWUEqPGTt"

# Your account's (the app owner's account's) access token and secret for your
# app can be found under the Authentication Tokens section of the
# Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
access_token = "835579733723205633-bEXZQZHANmkgV9G0H4Q0kwe9jHGLuyw"
access_token_secret = "N0yvkKet5Roc5JB737AVQKsoIIuZCtdwzspdVy2Iy3iuA"

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

# If the authentication was successful, this should print the
# screen name / username of the account
print(api.verify_credentials().screen_name)
