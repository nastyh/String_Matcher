# String_Matcher
String Matching done using fuzzywuzzy adopted for pd.DataFrame


## Dependencies and required packages:
pandas, numpy, fuzzywuzzy, nltk


## Method and use cases


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
create_matched_df(self, col_name, topN)
```
Returns a `pd.DataFrame` with two columns.
First column, *item_id*, contains values from `col_name`. Second column, *matches*, contains the best `topN` matches for this value from the same column. It doesn't include the value itself 
to the list of candidates, nor does it consider duplicates. 
Example: if there are 90 values in a column and all are unique, you will get a dataframe with 900 (90 * 10) rows.
If there are 90 values in a column but four are the same, you will get a dataframe with 870 (87 * 10) rows. The program will use the value the first time it sees it and will skip it next times.


## Bonus function

```
clean_column(self, col_name)
```
Takes a column `col_name`, applies `lower()` to it, removes NLTK's stopwords and adds a new column *col_name_clean* to the existing dataframe.
