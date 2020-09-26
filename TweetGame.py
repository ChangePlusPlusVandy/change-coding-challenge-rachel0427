import tweepy
# import the python file that contains token info
import Tokens
import random


# function to get tweets and add filtered text to a dictionary
def get_tweet(api, username):
    print("Getting tweets from @" + username + "...")
    # keep tweet list and dict to keep track tweets and plain text
    tweet_list = []
    tweet_dict = {}
    # initial request for 200 most recent tweets
    new_tweets = api.user_timeline(screen_name=username, count=200)
    # keep track of dict key
    num = 0
    # add text to tweet_dict
    for tweet in new_tweets:
        # get text part of tweet
        text = str(tweet.text.encode('utf-8'))
        # filter retweets, tweets that tag other users and tweets that contain urls
        if text.find("RT") == -1 and text.find("@") == -1 and \
                text.find("\\x") == -1 and text.find("https://") == -1:
            # add tweets to dictionary
            tweet_dict[num] = text[2:]
            num = num+1
    # add tweets to list
    tweet_list.extend(new_tweets)
    # save id of the last tweet added
    latest = tweet_list[-1].id - 1
    # while loop to keep getting tweets until maximum request number is reached
    while len(new_tweets) > 0:
        print(".")
        # request another 200 tweets
        new_tweets = api.user_timeline(screen_name=username, count=200, max_id=latest)
        tweet_list.extend(new_tweets)
        # repeat process
        latest = tweet_list[-1].id - 1
        for tweet in new_tweets:
            text = str(tweet.text.encode('utf-8'))
            if text.find("RT") == -1 and text.find("@") == -1 and text.find("\\x") == -1 and text.find("https://") == -1:
                #add tweets to dictionary
                tweet_dict[num] = text[2:]
                num = num + 1
    return tweet_dict


# function that verifies if the user correctly guess which user tweeted the tweet
# returns 0 if user guessed wrong, return 1 if user guessed correctly
def verify(user_input, dict_num, user1, user2):
    if dict_num == 1:
        if user_input.lower() == user1.lower():
            print("correct!")
            return 1
        else:
            print("Good guess, but the tweet was from @" + user1.lower() + "\n")
            return 0
    if dict_num == 2:
        if user_input.lower() == user2.lower():
            print("correct!")
            return 1
        else:
            print("Good guess, but the tweet was from @" + user2.lower() + "\n")
            return 0


# function to get user input of tweeter user names,
# return dictionary of user names
def get_user_name():
    user_name = {0: input("Please enter a Twitter user name(without the @ sign): "), 1:
        input("Please enter another Twitter user name: ")}
    # prompt user to enter two tweeter users names
    return user_name


# function that plays the game
def play():
    # connect to twitter api using keys and tokens
    auth = tweepy.OAuthHandler(Tokens.API_key, Tokens.API_secret_key)
    auth.set_access_token(Tokens.access_token, Tokens.access_token_secret)
    api = tweepy.API(auth)

    print("Welcome to tweet guessing game")
    # get user name dictionary
    user_name = get_user_name()
    # keep track of correct answers
    point = 0
    # keep track of attempt count
    count = 0
    # get dictionaries of both user's tweets
    answer = ""
    dict1 = get_tweet(api, user_name[0])
    tweet_count1 = len(dict1)
    dict2 = get_tweet(api, user_name[1])
    tweet_count2 = len(dict2)
    # start game
    print("Here is a tweets, please guess who they came from, @"
          + user_name[0] + " or @" + user_name[1] + " you don't need to add @ before your answer")
    # keep playing until user ends game
    while answer.lower() != "end":
        # generate random number to choose which user's tweet to display
        dict_rand = random.randint(1, 2)
        if dict_rand == 1:
            # generate random number to choose random tweet from user
            print("Tweet: " + dict1[random.randint(0, tweet_count1-1)])
        else:
            print("Tweet: " + dict2[random.randint(0, tweet_count2-1)])
        # prompt for user answer
        answer = input("Please enter your answer(enter \"END\" to quit game): ")
        # verify answer if user did not enter end
        if answer != "end":
            # keep track of correct answers
            point = point + verify(answer, dict_rand, user_name[0], user_name[1])
            # increment count
            count = count + 1
    # calculate missed answers
    miss = count - point
    print("Your Results: ")
    print("You answered " + str(point) + " correct and " + str(miss) + " wrong.")


# call play to start game
play()
