
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.streaming import StreamingContext
from functions import *
from operator import add
import pprint

from python.functions import normalize_text
from stopwords import Stopwords

spark_conf = SparkConf()
spark_conf.setMaster("local[1]")

spark_context = SparkContext(conf=spark_conf)
#spark_session = SparkSession(spark_context)

phrases = [
"""Apache Spark provides programmers with an application programming interface centered on a data structure called the resilient distributed dataset (RDD), a read-only multiset of data items distributed over a cluster of machines, that is maintained in a fault-tolerant way.[2] It was developed in response to limitations in the MapReduce cluster computing paradigm, which forces a particular linear dataflow structure on distributed programs: MapReduce programs read input data from disk, map a function across the data, reduce the results of the map, and store reduction results on disk. Spark's RDDs function as a working set for distributed programs that offers a (deliberately) restricted form of distributed shared memory.[3]""",
"""The availability of RDDs facilitates the implementation of both iterative algorithms, that visit their dataset multiple times in a loop, and interactive/exploratory data analysis, i.e., the repeated database-style querying of data. The latency of such applications (compared to Apache Hadoop, a popular MapReduce implementation) may be reduced by several orders of magnitude.[2][4] Among the class of iterative algorithms are the training algorithms for machine learning systems, which formed the initial impetus for developing Apache Spark.[5]""",
"""Apache Spark requires a cluster manager and a distributed storage system. For cluster management, Spark supports standalone (native Spark cluster), Hadoop YARN, or Apache Mesos.[6] For distributed storage, Spark can interface with a wide variety, including Hadoop Distributed File System (HDFS),[7] MapR File System (MapR-FS),[8] Cassandra,[9] OpenStack Swift, Amazon S3, Kudu, or a custom solution can be implemented. Spark also supports a pseudo-distributed local mode, usually used only for development or testing purposes, where distributed storage is not required and the local file system can be used instead; in such a scenario, Spark is run on a single machine with one executor per CPU core."""
]

stopwords = Stopwords()

rdd = spark_context.parallelize(phrases)
rdd = (rdd
        .map(normalize_text)
        .flatMap(lambda x: x.split())
        .filter(lambda w: not stopwords.is_stopword(w))
        .map(lambda x: (x, 1))
        .reduceByKey(add)
        .sortBy(lambda x: x[1])
)

results = rdd.count()
pprint.pprint(results)

