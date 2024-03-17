import datacompy
from pyspark.sql import SparkSession
import pandas as pd
import numpy as np

spark = SparkSession \
    .builder \
    .appName("how to read csv file") \
    .getOrCreate()

df1 = spark.read\
          .option("header",True)\
          .option("inferSchema",True)\
          .csv("/Users/ashok/PycharmProjects/recon_utility/src/main/data/Stores.csv")

df2 = spark.read\
          .option("header",True)\
          .option("inferSchema",True)\
          .csv("/Users/ashok/PycharmProjects/recon_utility/src/main/data/Stores_new.csv")
# print(spark.version)
df1.show()
df2.show(10)

base_df = df1.toPandas()
compare_df = df2.toPandas()

comparison = datacompy.Compare(base_df, compare_df, join_columns =  ['Store_ID'])

df_col_stats = comparison.column_stats

# df_html = pd.DataFrame.from_dict(df_col_stats).drop('match_column',axis=1)
# df_html.drop(df_html.columns[1],axis=1,inplace=True)
df_html = pd.DataFrame.from_dict(df_col_stats)

# print(df_html.to_html())

src_row_count = df1.count()
src_col_count = len(df1.columns)
tgt_row_count = df2.count()
tgt_col_count = len(df2.columns)

common_rows_count = comparison.intersect_rows.shape[0]
rows_in_src_only = comparison.df1_unq_rows.shape[0]
rows_in_tgt_only = comparison.df2_unq_rows.shape[0]
rows_having_mismatch = comparison.all_mismatch().shape[0]
row_having_no_mismatch = common_rows_count - rows_having_mismatch

common_cols_count = len(comparison.intersect_columns())
cols_in_src_only_count = len(comparison.df1_unq_columns())
cols_in_tgt_only = len(comparison.df2_unq_columns())
col_stats = comparison.column_stats
cols_having_no_mismatch = 0
cols_having_mismatch = 0
for element in col_stats:
    if(element['all_match']):
        cols_having_no_mismatch = cols_having_no_mismatch + 1
    else:
        cols_having_mismatch = cols_having_mismatch + 1


matched_keys = comparison.join_columns
absolute_tole = comparison.abs_tol
relative_tole = comparison.rel_tol

dupe_row_in_src = pd.merge(comparison.df1_unq_rows , comparison.intersect_rows,on=matched_keys, how='inner')
dupe_row_in_tgt = pd.merge(comparison.df2_unq_rows , comparison.intersect_rows,on=matched_keys, how='inner')
dupe_row_in_src_count = dupe_row_in_src.shape[0]
dupe_row_in_tgt = dupe_row_in_tgt.shape[0]
spaces_ignored = comparison.ignore_spaces

df_col_with_uneq_values_types = pd.DataFrame.from_dict(comparison.column_stats)
# print(df_col_with_uneq_values_types.to_html())


all_mismatch = comparison.all_mismatch()
print(all_mismatch)

total_cols_in_diff = len(all_mismatch.columns) - 1

def highlight_diff(x):
    styles = [''] * len(x)
    for i in range(1, len(x), 2):  # Starting from index 1 and comparing alternate adjacent columns
        if x.iloc[i] != x.iloc[i + 1]:
            styles[i] = 'background-color: yellow'
            styles[i + 1] = 'background-color: yellow'
    return styles

# Apply the custom function to the DataFrame
styled_df = all_mismatch.style.apply(highlight_diff,axis=1)

styled_df.hide(axis=0)

# Display the styled DataFrame
styled_html = styled_df._repr_html_()
print(styled_html)
