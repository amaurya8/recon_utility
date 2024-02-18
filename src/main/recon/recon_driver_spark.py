import datacompy
from pyspark.sql import SparkSession

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
# df1.show()
# df2.show(10)


base_df = df1
compare_df = df2

# base_df = df1.toPandas()
# compare_df = df2.toPandas()

# print(df1.schema)
comparison = datacompy.SparkCompare(spark, base_df, compare_df, join_columns =   [('Store_ID', 'Store_ID')])
# comparison = datacompy.Compare(base_df, compare_df, join_columns =  ['Store_ID'])
# print(comparison.report())

# comp = comparison.all_mismatch()
# print(comp)
# print(comparison.compare_unq_rows)
mis_df = comparison.rows_both_mismatch
print(comparison.rows_both_mismatch)


