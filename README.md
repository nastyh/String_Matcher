# String_Matcher
String Matching done using fuzzywuzzy adopted for pd.DataFrame


## Dependencies and required packages:
1. [pandas](https://pandas.pydata.org/)
2. [numpy](https://numpy.org/)
3. [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
4. [nltk](https://www.nltk.org/)


## Method and use cases

It uses a slightly optimized version of [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance#:~:text=Informally%2C%20the%20Levenshtein%20distance%20between,considered%20this%20distance%20in%201965.) with sorting and weighting performed. As a result, it distinguishes between "new Iphone" and "Iphone new" (unlike a plain-vanilla implementation of the distance). It's a no-frills implementation of a fairly computationally expensive method (it's average time complexity is O(NM), where N and M are lengths of respective strings) but, at the same, is a widely accepted method for fuzzy matching.  

That said, it works fairly well on strings up to 10-12 words where words can be placed in a random order. It is fairly common for item descriptions.

## Initialization:

```
def __init__(self, df)
```
Initialize with a `pd.DataFrame`


## Core functions:

```
create_matched_list(self, col_name, str_to_match, topN = 10)
```
Returns a list with `topN` best matches for `str_to_match` from column `col_name`.



```
create_matched_df(self, col_name, topN = 10)
```
Returns a `pd.DataFrame` with two columns.
First column, *item_id*, contains values from `col_name`. Second column, *matches*, contains the best `topN` matches for this value from the same column. It doesn't include the value itself to the list of candidates, nor does it consider duplicates. 
Example: if there are 90 values in a column and all are unique, you will get a dataframe with 900 (90 * 10) rows.
If there are 90 values in a column but four are the same, you will get a dataframe with 870 (87 * 10) rows. The program will use the value the first time it sees it and will skip it next times.


## Bonus function

```
clean_column(self, col_name)
```
Takes a column `col_name`, applies `lower()` to it, removes NLTK's stopwords and adds a new column *col_name_clean* to the existing dataframe.


## Provided files

`String_Matcher.py` -- core code  

`String_Matcher_int.ipynb` -- Jupyter Workbook with a working example
