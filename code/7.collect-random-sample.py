'''
This script collects a subset of tweets,
including only those that are about
climate protests and that have
higher engagement rates.
'''

import glob
import json
from multiprocessing import Pool
from os.path import isfile, basename
from os import remove
import pandas as pd
import random
import snscrape.modules.twitter as sntwitter


def make_query(conversation_id):
    """
    Builds a Twitter advanced search query for a given conversation ID.

    Args:
        conversation_id (str): The conversation ID for the Twitter search.

    Returns:
        str: The formatted query string for use with SNscraper, which includes a filter workaround
             to satisfy the advanced search's requirement of having at least two parameters.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """

	return f"conversation_id:{conversation_id} (filter:safe OR -filter:safe)" # the filter is only there to
																			  # fool advanced search, as it needs																	  # to have at least 2 params

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



def collect(tweets, conversation_id):
    """
    Extracts relevant information from the tweet stream retrieved by the query and returns it as a list of dictionaries.

    Args:
        tweets (generator): A generator object containing tweets to iterate through.
        conversation_id (str): The conversation ID of the tweet that originally received the replies.

    Returns:
        list: A list of dictionaries containing relevant tweet information, including a new field 'in_reply_to'
              that stores the conversation_id.

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
			'in_reply_to': conversation_id # adds the id of the tweet that originally got the reply

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
                      'fname': The desired output filename,
                      'conversation_id': The conversation ID for the Twitter search.

    Note: This docstring was created with the assistance of OpenAI's GPT-4 language model.
    """

	fname = query['fname']
	conversation_id = query['conversation_id']


	if isfile(fname):
		return
			
	print(fname)

	q = make_query(conversation_id)
	tweets = search(q)
	dataset = collect(tweets, conversation_id)
	#df = pd.DataFrame(dataset)

	save(dataset, fname)



def main():


	# Tweets that aren't about climate protests...	
	df = pd.read_csv("../../output/mvp/5.merged_dataframes/no-keywords.csv", sep="|")

	#...and also have high engagement
	df = df[df.percentile_for_total_engagement <= 1]

	# We will randomly select n tweets
	sample = 100
	df = df.sample(sample)

	# Gets the conversation ids for those
	conversation_ids = df.conversation_id.unique().tolist()
	conversation_ids = [f'{conversation_id}.json' for conversation_id in conversation_ids]

	# Remove all the tweets that are not in this run of the sample
	downloaded_tweets = glob.glob(f'../../output/mvp/7.random_sample/*.json')
	
	for downloaded_tweet in downloaded_tweets:

		if basename(downloaded_tweet) not in conversation_ids:
			remove(downloaded_tweet)


	# Saves the newly collected files
	queries = []
	for conversation_id in conversation_ids:

		fname = f'../../output/mvp/7.random_sample/{conversation_id}'
		query = {'conversation_id':conversation_id[:-5], 'fname': fname}

		queries.append(query)

	
	
	# Executes 8 queries in paralel
	with Pool(8) as p:
		p.map(scrape, queries)



if __name__ == "__main__":
	main()                                                              