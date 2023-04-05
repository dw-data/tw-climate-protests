#!/usr/bin/env python
# coding: utf-8

'''
This scripts uses the SNScrape to collect all tweets published by our outlets of interest since
20/08/2018, when Greta Thurnberg first skipped school to protest.
'''

# Code below adapted from https://datasciencedojo.com/blog/scrape-twitter-data-using-sncrape/

import pandas as pd
from pprint import pprint
import numpy as np
import snscrape.modules.twitter as sntwitter
import datetime
from tqdm.notebook import tqdm_notebook
import seaborn as sns
import matplotlib.pyplot as plt
import json
from os.path import isfile
from multiprocessing import Pool

def make_query(text, username=None, since=None, until=None, retweet=True, replies=True):
    """
    Builds a Twitter advanced search query for use with SNscraper.

    Args:
        text (str): The text to search for in the tweets.
        username (str, optional): The username to search tweets from. Defaults to None.
        since (str, optional): The start date for the search, in the format 'YYYY-MM-DD'. Defaults to None.
        until (str, optional): The end date for the search, in the format 'YYYY-MM-DD'. Defaults to None.
        retweet (bool, optional): Include retweets in the search results. Defaults to True.
        replies (bool, optional): Include replies in the search results. Defaults to True.

    Returns:
        str: The formatted query string for use with SNscraper.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """
    
    q = text

    if username:
        q += f" from:{username}"

    if until:
        q += f" until:{until}"
    else:
        until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
        q += f" until:{until}"

    if since:
        q += f" since:{since}"

    if not retweet:
        q += f" exclude:retweets"

    if not replies:
        q += f" exclude:replies"

    if username and text:
        filename = f"{since}_{until}_{username}_{text}.csv"

    elif username:
        filename = f"{since}_{until}_{username}.csv"

    else:
        filename = f"{since}_{until}_{text}.csv"

    return q.strip()


def search(q):
    """
    Uses SNscrape to perform a Twitter search query and retrieves the tweets of interest.
    Args:
        q (str): The formatted query string for use with SNscraper.

    Returns:
        generator: A generator object to iterate through the retrieved tweets.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """
    
    # Sends the request
    r = sntwitter.TwitterSearchScraper(q) 
    
    # Creates a generator object to iterate through
    tweets = r.get_items()
    
    return tweets



def collect(tweets):
    """
    Extracts relevant information from the tweet stream retrieved by the 
    query and returns it as a list of dictionaries.

    Args:
        tweets (generator): A generator object containing tweets to iterate through.

    Returns:
        list: A list of dictionaries containing relevant tweet information.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """
        
    # Gets the information of interest for each tweet
    dataset = []
    for index, tweet in enumerate(tweets):
        
        progress_string = f"Fetching tweet {index}".ljust(20)
        print(progress_string , sep="\r")
        
        #pprint(tweet)

        data = {
            'url': tweet.url,
            'raw_content': tweet.rawContent,
            'tweet_id': tweet.id,
            'user': tweet.user.username,
            'conversation_id': tweet.conversationId,
            'like_count': tweet.likeCount,
            'reply_count': tweet.replyCount,
            'quote_count': tweet.quoteCount,
            'retweet_count': tweet.retweetCount,
            'date': str(tweet.date),
            #'lang': tweet.lang,
            #'source': tweet.source,
            #'source_url': tweet.sourceUrl,
            #'source_label': tweet.sourceLabel,
            #'links': tweet.links,
            #'media': tweet.media,
#             'retweeted_tweet': tweet.retweetedTweet,
#             'quoted_tweet': tweet.quotedTweet,
#             'in_reply_to_tweet_id': tweet.inReplyToTweetId,
#             'in_reply_to_user': tweet.inReplyToUser,
#             'mentioned_users': tweet.mentionedUsers,
#             'coordinates': tweet.coordinates,
#             'place': tweet.place,
#             'hashtag': tweet.hashtags,
#             'cashtags': tweet.cashtags,
            #'card': tweet.card


        }

        dataset.append(data)
        
    return dataset


def save(dataset, filename):
    """
    Saves the dataset as a JSON file with the specified filename.

    Args:
        dataset (list): A list of dictionaries containing relevant tweet information.
        filename (str): The desired filename for the output JSON file.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """

    
    with open(filename, 'w+') as f:
        json.dump(dataset, f)


def scrape(query):
     """
    Executes the scraper with the information for a query.

    Args:
        query (dict): A dictionary containing the following keys:
                      'username': The Twitter username to scrape,
                      'fname': The desired output filename,
                      'since': The start date for the search in the format 'YYYY-MM-DD',
                      'until': The end date for the search in the format 'YYYY-MM-DD'.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """


    username = query['username']
    fname = query['fname']
    since = query['since']
    until = query['until']

    if isfile(fname):
        return
            
    print(fname)

    q = make_query('', username=username, since=since, until=until, retweet=False, replies=False)
    tweets = search(q)
    dataset = collect(tweets)
    #df = pd.DataFrame(dataset)

    save(dataset, fname)

    #return df


def main():

    # Those are among the 30 twitter accounts with the most followers
    usernames = ['rt_com',
                 'Telegraph',
                 'newsweek',
                 'bbcafrica',
                 'independent',
                 'guardiannews',
                 'france24',
                 'cnbc',
                 'politico',
                 'SkyNewsBreak',
                 'ft',
                 'ajenglish',
                 'skynews',
                 'BreakingNews',
                 'guardian',
                 'huffpost',
                 'xhnews',
                 'ap',
                 'ndtv',
                 'abc',
                 'time', 
                 'washingtonpost',
                 'wsj',
                 'reuters',
                 'theeconomist',
                 'bbcworld',
                 'bbcbreaking',
                 'nytimes',
                 'cnn',
                 'cnnbrk'
                ]

    # Start with the biggest channels
    usernames.reverse()

    # For each user name, create a query
    queries = []
    for username in usernames:
                
            since = '2018-08-20'
            until = '2023-02-20'

            fname = f'../../output/mvp/{username}_{since}_{until}.json'

            query = {'username': username, 'since': since, 'until': until, 'fname': fname}

            queries.append(query)
            

    # Executes 8 queries in paralel
    with Pool(8) as p:
        p.map(scrape, queries)

    # dfs = []

    #dfs.append(df)


    # # Remove newlines within tweets
    # dfs['raw_content'] = dfs.raw_content.str.replace("\n", " ")

    # dfs.to_csv("../../output/all-tweets.csv", sep=";")


if __name__ == "__main__":
    main()