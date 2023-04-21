# Climate Protests in Twitter

Idea: [Serdar Vardar](https://twitter.com/serdarvardar_?lang=en)
Data analysis and visualization: [Rodrigo Menegat Schuinski](https://twitter.com/RodrigoMenegat)
Research and writing: [Serdar Vardar](https://twitter.com/serdarvardar_?lang=en)

You can read the story [here](https://www.dw.com/a-65383936)

## Project overview

This repository contains the source code for DW's story about climate protests on Twitter.

---

## Brief methodological description

For this story, we collected all tweets published between Aug. 20, 2018 and Feb. 18, 2023. 
by the 30 English-language news organizations with the most followers on Twitter.

We then computed the total engagement numbers (that is, the sum of retweets, quote tweets, replies and likes received by each tweet) for each post. We also computed a relative measurement of engagement – that is, in which percentile of the total engagement metric each tweet was, in comparison to the tweets published by the same news organization in the same week.

All of the nearly 4,3 million tweets retrieved were then searched for keywords related to climate and environmental protests. As a result, 3,636 tweets were marked as of potential interest. Those tweets were then manually reviewed in order to discard any false positives. 

Moreover, the tweets that really refered to climate change were classified in two distinct categories: "non-disruptive" and "disruptive". The "non-disruptive" label refers to tweets about acts such as defacing monuments, buildings or art pieces, storming public buildings, occupying public spaces without clearence, blocking traffic, clashing with security forces, interrupting events, and similar actions. The "disruptive" label refers to tweets about activist participation in institutional forums, public speeches, interviews by activists, pacific rallies, artistic interventions, and the like.

We then selected all the tweets from this two categories that were among the highest engagement percentile, as well as a random sample of high engagement tweets that didn't mention climate change. All the direct replies to those tweets were also collected.

We then used two language processing models (available [here](https://huggingface.co/papluca/xlm-roberta-base-language-detection) and [here](https://huggingface.co/siebert/sentiment-roberta-large-english), respectively) to analyze those replies. We first removed from the data all tweets that were in a language other than English. Then, we classified each reply as displaying positive or negative sentiment. The results of the sentiment analysis were then used to measure how much negativity each of the original tweets generated.

A detailed description of the process can be found below.

---

## Code structure

### Data preparation

#### 1.collect.py
This script collects content and engagement numbers for the tweets we used in the analysis using the Python package SNscraper. It saves the data for each of the news organizations into a separate JSON file.

#### 2.concatenate-and-compute.ipynb
In this notebook, we read the JSON files saved previously, joining them together and turining them into a pandas dataframe. Then, we compute the aggregate fields that were used for the data analysis later – most importantly, the relative engagement rates of each tweet when compared to the ones published in the same week by the same news organization.

#### 3.detect-keywords.ipynb
In this script, we define two lists of keywords, one related to climate change and the other related to protests in general. We then use it to detect tweets that mention at least one word in both lists.

#### 4.manually-categorize.py
This script was used as a helper to manually classify the tweets selected above into three categories.
	a. *"nd"*: tweets that mention non-disruptive climate protests (such as activist participation in institutional forums, public speeches, interviews by activists, rallies, and artistic interventions).
	b. *"d"*: tweets that mention disruptive ones (such as defacing monuments or art pieces, storming public buildings, occupying public spaces without clearence, blocking traffic, clashes with security forces, disruption of events and rallies by groups that promote civil desobedience tactics). 
	c. **"fp"**: tweets that were selected because they mention specific keywords, but don't actually refer to climate protests.

#### 5.merge-results.ipynb
Here we join the manual classification and the original dataframe, adding the manual classification as new columns. The script saves the tweets that have keywords and that don't have keywords in different CSV files.

#### 6.collect-top-n-replies.py
This script collects all the replies to tweets in the "nd" and "d" categories that were among the top 1% with the most engagement of their news organizations in the week that they were published.

#### 7.collect-random-sample.py
This script collects all the replies to a random sample of 100 similarly high engagement tweets that aren't about climate protests.

#### 8.prepare-dfs-for-sentiment-analysis.ipynb
This notebooks takes the tweets collected in steps 6 and 7, formats them and saves them as CSVs that can go through a sentiment analysis algorithm.

---

**The following steps were run in a Google Colab environment, since they were computationally heavy.** To do so, the files in the output directory `8.dfs-for-sentiment-analysis` were uploaded to Google Drive and accessed programatically using Google Colab notebooks. In this repository, you can find copies of the notebooks that ran in Google Colab environment.

#### 9.high_engagement_language_detect.ipynb
This script uses a natural language processing model to detect the language of the replies to the high engagement climate protest tweets. The model used is `papluca/xlm-roberta-base-language-detection`, which is available for public use at [HuggingFace](https://huggingface.co/papluca/xlm-roberta-base-language-detection).

#### 10.high_engagement_sentiment_analysis.ipynb
This script uses another Hugging Face model to classify the English language high engagement climate protest tweets into POSITIVE and NEGATIVE. The model used was `siebert/sentiment-roberta-large-english`, which is available for public use [here](https://huggingface.co/siebert/sentiment-roberta-large-english).

#### 11.control_language_detect.ipynb
Almost identical to script 9, but it runs the NLP model on the replies to the randomly selected tweets.

#### 12.control_sentiment_analysis.ipynb
Almost identical to script 10, but it runs the NLP model on the replies to the randomly selected tweets.

#### 13.export_sentiment_analysis_dfs.ipynb
Creates CSVs for each one of the sentiment analysis, so we could later analyze and visualize the data.

---

### Analysis and data visualization

#### a.engagement-over-time.ipynb
In this script, we discover and visualize how the coverage and engagement of climate protest tweets changed over time.

#### b.engagement-distribution.ipynb
This script prepares the data for use in the swarm plots that show the distribution of tweets according to their engagement levels.

#### c.greta-thunberg.ipynb
Simple calculation of how many times Greta Thunberg is mentioned on each kind of climate protest tweet.

#### d.sentiment-analysis.ipynb
Analyzes the results of the sentiment analysis and exports the data for dataviz. Also exports SVGs for the data visualization.

#### viz.engagement-over-time
Source code of the d3.js chart that shows how engagement to climate protest tweets changed over time.

#### viz.engagement-distribution
Source code of the d3.js chart that generate swarmplots showing the distribution of engagement ratios for each category.

#### viz.greta-thunberg
Source code of the d3.js chart that shows how Greta Thunberg is mentioned in the majority of high engagement protest tweets.

## Raw data

If you would like to obtain the raw data behind the project, please email data-team[at]dw.com
