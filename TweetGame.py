import sys
import tweepy
import Tokens
import datetime, time

auth = tweepy.OAuthHandler(Tokens.API_key, Tokens.API_secret_key)
auth.set_access_token(Tokens.access_token, Tokens.access_token_secret)
api = tweepy.API(auth)

fileDict = {}

# function to get tweets
def get_tweets(api, username, file_dict):
    # get tweets from user
    tweets = api.user_timeline(username)
    # create and write to outFile
    outFile = username + ".txt"
    s = open(outFile, "w+")
    for tweet in tweets:
        s.write(str(tweet.text.encode('utf-8')) + "\n")
    s.close()
    # save file in file dictionary
    file_dict[outFile] = s


# start program
print("Welcome to game")
# get unfiltered twees from elon musk
get_tweets(api, "elonmusk", fileDict)
# get unfiltered tweets from kanye west
get_tweets(api, "kanyewest", fileDict)






