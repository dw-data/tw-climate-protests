#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import json

def classify_data(csv_file_path):
    """
    This function reads data from a CSV file, filters out rows where 'has_both_keywords' is False,
    and asks the user for input to classify each row as "d" (disruptive), "nd" (non-disruptive),
    or "fp" (false positive). It then creates a JSON file with the user's answer 
    for each row and saves it in the `output/4.manual-classification directory 

    Args:
        csv_file_path (str): The path to the CSV file containing the data to be classified.

    Returns:
        None
    """
    # create classification directory if it does not exist
    dir_path = '../../output/mvp/4.manual_classification/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # read data from csv file
    df = pd.read_csv(csv_file_path, sep="|")

    # filter out rows where 'has_both_keywords' is False
    df = df[df['has_both_keywords']]

    # loop through rows and classify each one
    for i, row in df.iterrows():
        # check if classification file already exists
        file_path = os.path.join(dir_path, f'{i}.json')
        if os.path.exists(file_path):
            continue

        # print row information and ask for user input
        print(f'Raw content:\n{row["raw_content"]}\n')
        print(f'Climate keywords:\n{row["climate_tokens"]}\n')
        print(f'Protest keywords:\n{row["protest_tokens"]}\n')
        print(f'Date:\n{row["date_str"]}\n')
        print(f'\n{row["url"]}\n')

        while True:
            user_input = input(f'Classification for row {i} out of {df.shape[0]}: ')
            if user_input in ['d', 'nd', 'fp']:
                break
            else:
                print('Invalid input. Valid options are "d" (disruptive), "nd" (non-disruptive), and "fp" (false positive).')

        # create json file with user input
        with open(file_path, 'w') as f:
            json.dump({'classification': user_input}, f)

        print("\n *** \n")


def main():
    classify_data(csv_file_path="../../output/mvp/3.tweets_with_keyword_detection/tweets-with-keywords.csv")


if __name__ == "__main__":
    main()



