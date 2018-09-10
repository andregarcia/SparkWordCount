
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.streaming import StreamingContext
from functions import *
from operator import add
import pprint
from pyspark.sql import SQLContext

from python.functions import normalize_text
from stopwords import Stopwords

spark_conf = SparkConf()
spark_conf.setMaster("local[4]")

spark_context = SparkContext(conf=spark_conf)

sql_context = SQLContext(spark_context)

stopwords = Stopwords()

df = sql_context.read.format('com.databricks.spark.xml')\
        .options(rowTag='page')\
        .load('/home/andregarcia/Downloads/wikipedia/ptwiki-20180901-pages-articles-multistream.xml')

rdd = df.select("revision.text")\
        .rdd \
        .map(lambda row: row.text._VALUE)\
        .filter(lambda x: x and type(x)==str)\
        .map(normalize_text)\
        .flatMap(lambda x: x.split()) \
        .filter(lambda x: x and type(x) == str) \
        .filter(lambda w: not stopwords.is_stopword(w))\
        .map(lambda x: (x, 1))\
        .reduceByKey(add)\
        #.sortBy(lambda x: x[1], ascending=True)


results = rdd.takeOrdered(100, lambda x: -x[1])
pprint.pprint(results)

