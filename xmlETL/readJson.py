import sys, os
cwd = os.getcwd()
from pathlib import Path
parentPath = Path(cwd).parent
parentPath = str(parentPath)

jsonLocation = parentPath+"\\xml_json\\"

print(jsonLocation)
# ------------------------------------------
import pyspark
from pyspark import SparkConf
from pyspark import SparkContext
sc =SparkContext()

# You can configure the SparkContext

conf = SparkConf()
conf.set('spark.local.dir', '/remote/data/match/spark')
conf.set('spark.sql.shuffle.partitions', '2100')
# SparkContext.setSystemProperty('spark.executor.memory', '10g')
# SparkContext.setSystemProperty('spark.driver.memory', '10g')
# sc = SparkContext(appName='mm_exp', conf=conf)
sqlContext = pyspark.SQLContext(sc)

sdf = sqlContext.read.json(jsonLocation)

sdf.printSchema()