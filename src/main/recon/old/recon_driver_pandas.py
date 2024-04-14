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
# # print(spark.version)
# df1.show()
# df2.show(10)

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

summary_chart_data = [src_col_count,src_col_count,tgt_row_count,tgt_col_count]
row_summary_data = [common_rows_count,rows_in_src_only,rows_in_tgt_only,row_having_no_mismatch,rows_having_mismatch]
col_summary_data = [common_cols_count,cols_in_src_only_count,cols_in_tgt_only,cols_having_no_mismatch,cols_having_mismatch]

matched_keys = comparison.join_columns.__str__()
absolute_tole = str(comparison.abs_tol)
relative_tole = str(comparison.rel_tol)

dupe_row_in_src = pd.merge(comparison.df1_unq_rows , comparison.intersect_rows,on='store_id', how='inner')
dupe_row_in_tgt = pd.merge(comparison.df2_unq_rows , comparison.intersect_rows,on='store_id', how='inner')
dupe_row_in_src_count = dupe_row_in_src.shape[0]
dupe_row_in_tgt = dupe_row_in_tgt.shape[0]
spaces_ignored = comparison.ignore_spaces

df_col_with_uneq_values_types = pd.DataFrame.from_dict(comparison.column_stats)
# print(df_col_with_uneq_values_types.to_html())

all_mismatch = comparison.all_mismatch()

def highlight_diff(x):
    styles = [''] * len(x)
    for i in range(1, len(x), 2):  # Starting from index 1 and comparing alternate adjacent columns
        if x.iloc[i] != x.iloc[i + 1]:
            styles[i] = 'background-color: #FF6347'
            styles[i + 1] = 'background-color: #FF6347'
    return styles

# Apply the custom function to the DataFrame
styled_df = all_mismatch.style.apply(highlight_diff,axis=1)

styled_df.hide(axis=0)

# Display the styled DataFrame
styled_html = styled_df._repr_html_()
# print(styled_html)

########################### generating report ##########################

with open('/Users/ashok/PycharmProjects/recon_utility/src/main/recon/old/recon_report_tmpl12.html', 'r') as input_report_file , open('recon_report_final.html', 'w') as output_report_file:
    html_report = input_report_file.read()
    html_report = html_report.replace("#absolute_tole#", absolute_tole)
    html_report = html_report.replace("#relative_tole#", relative_tole)
    html_report = html_report.replace("#matched_keys#", matched_keys)
    html_report = html_report.replace("#Columns with un-eq values / types#", df_col_with_uneq_values_types.to_html().__str__())
    html_report = html_report.replace("#Rows with un-eq values#", styled_html)
    html_report = html_report.replace("#Rows Only In Src#", comparison.df1_unq_rows.to_html().__str__())
    html_report = html_report.replace("#Rows Only In Tgt#", comparison.df2_unq_rows.to_html().__str__())
    html_report = html_report.replace("#Summary Chart#", summary_chart_data.__str__())
    html_report = html_report.replace("#Row Summary#", row_summary_data.__str__())
    html_report = html_report.replace("#Column Summary#", col_summary_data.__str__())

    output_report_file.write(html_report)
