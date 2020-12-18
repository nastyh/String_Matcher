#  GO TO THE PROVIDED WORKBOOK TO SEE A WORKING EXAMPLE
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
import glob
stop = stopwords.words('english')
from collections import defaultdict

class String_Matcher():
    """
    Class uses the Levenstein distance to find similar strings.
    Quick and dirty analysis shows that order of words doesn't make much difference, as well as, a removal of punctuation and stop-words.
    However, light cleaning is possible via clean_column()

    How to use:
    sm = String_Matcher(filepath)
    l = sm.created_matched_list('item_title', 'ipod') will create a list with the top 10 matches for the query 'ipod' from the column df['item_title'] 
    matched_df = sm.create_matched_df('item_title') will create a dataframe with two columns. The first column are item titles, the second column are the top 10
    matches selected from the same column. 
    """

    def __init__(self, filepath):
        """
        filepath: string with a path to the folder containing .txt files to be processed
        """
        l = [pd.read_csv(filename, header = None, sep = '\t', names = ['item_id', 'site', 'category_id', 'item_title'])\
            for filename in glob.glob(filepath + '/*.txt')]
        self.df = pd.concat(l, axis = 0)


    def clean_column(self, col_name):
        """
        (Optional: doesn't seem to change the matching quality much)
        Takes column 'col_name' and creates a new column 'col_name_clean'
        where all characters are in the lower case and stop words (using nltk.corpus) are removed

        col_name: string
        """
        self.df[col_name + str('_clean')] = self.df[col_name].str.lower()
        self.df[col_name + str('_clean')].apply(lambda x: [item for item in x if item not in stop])
        return self.df


    def create_matched_list(self, col_name, str_to_match, topN = 10):
        """
        Returns topN matches as a list of strings from a column df[col_name] for a provided string str_to_match
        One caveat: it looks across all the files (because they're concatenated into one dataframe) that might or might not
        be a good idea depending on the context (for files containing info about different categories, it's probably bad).
        But building a logic for separate files was taking time.

        col_name: string
        topN (optional): integer. Default is 10
        """
        res, choices, output = [], [], []
        for item in self.df[col_name].unique(): 
            choices.append(item)
        res = process.extract(str_to_match, choices, limit = topN)
        for line in res:
            output.append(line[0])
        return output


    def create_matched_df(self, col_name, topN = 10):
        """
        Returns pd.DataFrame with two columns: 'item_title' and 'matches.'
        For every item_title, there are 10 matches. IMPORTANT: it considers only unique values.
        If a dataframe consists of 10 titles but two of them are similar, it will return 90 (9 * 10) rows. This happens to the mp3 dataset
        One caveat: it looks across all the files (because they're concatenated into one dataframe) that might or might not
        be a good idea depending on the context (for files containing info about different categories, it's probably bad).
        But building a logic with separate files was taking time.
        The provided score takes care of punctuation and word order.

        col_name: string
        topN (optional): integer. Default is 10
        """
        d = defaultdict(list)
        for k, v in enumerate(self.df[col_name].unique()):
            curr_res = []
            choices = list(self.df[col_name].iloc[:k]) + list(self.df[col_name].iloc[k + 1:])
            curr_res = process.extract(v, choices, limit = topN, scorer = fuzz.token_sort_ratio)
            for ix in range(len(curr_res)):
                d[v].append(curr_res[ix][0])
        df_from_d = pd.DataFrame.from_dict(d, orient = 'index', columns = ['Top1', 'Top2', 'Top3', 'Top4', 'Top5','Top6', 'Top7', 'Top8', 'Top9', 'Top10'])
        df_from_d_stacked = df_from_d.stack().reset_index()
        df_from_d_stacked.drop('level_1', axis = 1, inplace = True)
        df_from_d_stacked.rename(columns = {"level_0": "item_id", 0: "matches"}, inplace = True)
        return df_from_d_stacked


        def save_to_csv(self, df, filepath, filename):
            """
            Saves the provided dataset to the folder defined in 'filepath' with the name defined in 'filename'

            df: pd.DataFrame
            filepath: string
            filename: string
            """
            df.to_csv(filepath + "/" + filename)
