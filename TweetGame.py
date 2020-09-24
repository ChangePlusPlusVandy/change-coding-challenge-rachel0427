import sys
import tweepy
import Tokens
import random
import datetime, time

auth = tweepy.OAuthHandler(Tokens.API_key, Tokens.API_secret_key)
auth.set_access_token(Tokens.access_token, Tokens.access_token_secret)
api = tweepy.API(auth)

fileDict = {}


# function to get tweets
def get_tweets(api, username):
    # keep dictionary to store tweets
    tweet_dict = {}
    num = 0
    # get tweets from user
    tweets = api.user_timeline(username)
    for tweet in tweets:
        # add tweets to dictionary
        tweet_dict[num] = (str(tweet.text.encode('utf-8')) + "\n")
        num = num + 1
    return tweet_dict


# function to get tweets
def get_tweets_f(api, username, file_dict):
    # get tweets from user
    tweets = api.user_timeline(username)
    # create and write to outFile
    out_file = username + ".txt"
    s = open(out_file, "w+")
    for tweet in tweets:
        s.write(str(tweet.text.encode('utf-8')) + "\n")
        num = num + 1
    s.close()
    # save file in file dictionary
    file_dict[out_file] = s


def varify(user_input, dict_num, user1, user2):
    if dict_num == 1:
        if user_input.lower().replace(" ", "") == user1.lower():
            print("correct!")
            return 1
        else:
            print("Good guess, but the tweet was from " + user1.lower())
            return 0
    if dict_num == 2:
        if user_input.lower().replace(" ", "") == user2.lower():
            print("correct!")
            return 1
        else:
            print("Good guess, but the tweet was from " + user2.lower())
            return 0


def play():
    print("Welcome to tweet guessing game")
    input1 = input("Please enter a Twitter user name: ")
    input2 = input("Please enter another Twitter user name: ")
    point = 0
    count = 0
    answer = ""
    user1 = input1.replace(" ", "")
    user2 = input2.replace(" ", "")
    dict1 = get_tweets(api, user1)
    tweet_count1 = len(dict1)
    dict2 = get_tweets(api, user2)
    tweet_count2 = len(dict2)
    print("Here is a tweets, please guess who they came from, @"
          + user1 + " or @" + user2)
    while answer.lower() != "end":
        dict_rand = random.randint(1, 2)
        if dict_rand == 1:
            print("Tweet: " + dict1[random.randint(0, tweet_count1-1)])
        else:
            print("Tweet: " + dict2[random.randint(0, tweet_count2-1)])
        answer = input("Please enter your answer(enter \"END\" to quit game): ")
        point = point + varify(answer, dict_rand, user1, user2)
        count = count + 1
        miss = count - point
    print("You got " + str(point) + " right and " + str(miss) + " wrong.")


play()






















