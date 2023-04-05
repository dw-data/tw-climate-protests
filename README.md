# Climate Protests in Twitter

## Project overview

...
...
...


## Code structure

### Data preparation

#### 1-collect.py
This script will collect the content and engagement numbers for the tweets we used in the analysis using the Python package SNscraper. It saves data for each of the relevant accounts into a separate JSON file.

#### 2.concatenate-and-compute.ipynb
In this notebook, we read the JSON files saved previously, joining them together and turining them into a pandas dataframe. Then, we compute the aggregate fields that were used for the data analysis later – namely, the relative engagement rates of each tweet when compared to the ones published in the same week by the same news organization.

#### 3.detect-keywords.ipynb
In this script, we define two lists of keywords, one related to climate change and the other related to protests in general. We then use it to detect tweets that mention at least one word in each list at each time. This approach allows to find tweets that are not only about protests in general or environmental issues in general. Instead, we select only those that mention both. It also allow us to lower the number of false positives detected.

#### 4.manually-categorize.py
This script prompts the user to manually classify the tweets selected above into three categories.
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

**The following steps were run in a Google Colab environment, since they were computationally heavy.** To do so, the files in the output directory `8.dfs-for-sentiment-analysis` were uploaded to Google Drive and accessed programatically using Google Colab notebooks. You can find copies of the notebooks that ran in Google Colab in the repository.

#### 9.high_engagement_language_detect.ipynb
This script uses a natural language processing model to detect the language of the replies to the high engagement climate protest tweets. The model used is `papluca/xlm-roberta-base-language-detection`, which is available for public use at [HuggingFace](https://huggingface.co/papluca/xlm-roberta-base-language-detection).

#### 10.high_engagement_sentiment_analysis.ipynb
This script uses another Hugging Face model to classify the English language high engagement climate protest tweets into POSITIVE and NEGATIVE. The model used was `siebert/sentiment-roberta-large-english`, which is available for public use [here](https://huggingface.co/siebert/sentiment-roberta-large-english).

#### 11.control_language_detect.ipynb
Almost identical to script 9, but it runs the NLP model on the replies to the randomly selected tweets.

#### 12.control_sentiment_analysis.ipynb
Almost identical to script 10, but it runs the NLP model on the replies to the randomly selected tweets.

#### 13.export_sentiment_analysis_dfs.ipynb
Creates CSVs for each one of the sentiment analysis, so we can analyze and visualize the data.

### Analysis and data visualization

#### a.engagement-over-time.ipynb
In this script, we discover and visualize how the coverage and engagement of climate protest tweets changed over time.

#### b.engagement-distribution.ipynb
This script prepares the data for use in the swarm plots that show the distribution of tweets according to their engagement levels.

#### c.greta-is-everywhere.ipynb
Simple calculation of how many times Greta Thunberg is mentioned on each kind of climate protest tweet.

#### d.sentiment-analysis.ipynb
Analyzes the results of the sentiment analysis and exports the data for dataviz. Also exports SVGs for the data visualization.

#### viz.engagement-over-time
Source code of the d3.js chart that shows how engagement to climate protest tweets changed over time.

#### viz.engagement-distribution
Source code of the d3.js chart that generate swarmplots showing the distribution of engagement ratios for each category.

#### viz.greta-thunberg
Source code of the d3.js chart that shows how Greta Thunberg is mentioned in the majority of high engagement protest tweets.
