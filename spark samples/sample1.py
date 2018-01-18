import random
import findspark

findspark.init("C:\spark-2.2.1-bin-hadoop2.7")
from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName('MyFirstStandaloneApp')
sc = SparkContext(conf=conf)
NUM_SAMPLES = 20
def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = sc.parallelize(range(0, NUM_SAMPLES)) \
             .filter(inside).count()
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))