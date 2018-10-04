# part 2: social media mining with NLP analysis
# Author: Qianying Yu, Tzu-Chien Fu, Sheng-Feng Hsu

import tweepy
import re
from textblob import TextBlob

def get_tweet(filename, kw):
    '''
    This function is to get tweets from Twitter API
    :param filename: text files to store tweets during finals
    :param kw: keywords for searching relevant tweets

    '''
    consumer_key = 'bjP9KQG6vJrKZ6Hzd4zK3kNxt'
    consumer_secret = 'mKmQzlYLqBOb2diyv1j2vtPs607XfahzhkhEAqhz81JRg8FHz2'
    access_token = '913499009142181888-esMx8bQiUngrvfLr9P7QKjchRk24j7G'
    access_token_secret = '8esLh5Pup0yfKoIvQXm2BEFxaHLw0knUvtG4VZjjvkHpt'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    txtfile = open(filename, 'w')
    txtfile.close()


    for tweet in tweepy.Cursor(api.search,q = kw,count=100,
                               lang="en",
                               since="2018-05-31").items():
        #print (tweet.created_at, tweet.text)
        txtfile.write('{' + str(tweet.created_at) + ':' + str(tweet.text) + '}' + '\n')

def clean_tweet(tweet):
    '''
    This function is to avoid unuseful information in tweets
    :param tweet: original tweets
    :return: cleaned tweets
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    This function is to get the result of sentiment analysis of each tweet
    :param tweet: cleaned tweets
    :return: sentiment of each tweet
    '''
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def sentiment_analysis(filename):
    '''
    This function is to calculate the number of tweets with different attitude
    :param filename: collected data of each player
    :return: count of sentiment analysis
    '''
    data = open(filename, 'r')
    positive_cnt = 0
    neutral_cnt = 0
    negative_cnt = 0
    tot_cnt = 0
    for tweet in data:
        clean = clean_tweet(tweet)
        sentiment = get_tweet_sentiment(clean)
        if sentiment == 'positive':
            positive_cnt += 1
        elif sentiment == 'neutral':
            neutral_cnt += 1
        else:
            negative_cnt += 1
        tot_cnt += 1

    return tot_cnt, positive_cnt, neutral_cnt, negative_cnt

def main():
    get_tweet('../Dataset/LeBron_mvp.txt', 'LeBron MVP' or 'lbj MVP')
    get_tweet('../Dataset/curry_mvp.txt', 'curry MVP')
    get_tweet('../Dataset/durant_mvp.txt', 'Durant MVP' or 'KD MVP')

    print('curry', sentiment_analysis('../Dataset/curry_mvp.txt'))
    print('durant', sentiment_analysis('../Dataset/durant_mvp.txt'))
    print('LeBron', sentiment_analysis('../Dataset/LeBron_mvp.txt'))

if __name__ == '__main__':
    main()
