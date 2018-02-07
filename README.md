# 4thYearProject
College 4th/Final year project 

## Requirements 
   - Nvidia Cuda libraries and tools
   - Pycuda
   - Numpy
   - Beatifulsoup library
   - Spark
   - Hadoop
   - Findspark (python lib)
   (I am running Spark 2.2.1 and Hadoop 2.7.5)
   
## TO RUN MASTER branch
To run full program use `python readList.py`
Please see sample output below

![alt text](https://github.com/GLalor/Vanilla-Option-Pricer/blob/master/output.PNG "Sample output")

### BUG
  Problems can arrise if Yahoo hasnt removed a past date
  
## TO RUN MULTIPROSS branch
Run code on machine with **NVidia GPU installed**<br />
To run full program use `python readList.py`<br />
Output will be printed to a JSON file<br />

## TO RUN SPARK branch
Run code on machine with **Spark, Hadoop and findspark installed**<br />
User will first need to modify Line 6 to point to there installation of spark
   `findspark.init("C:\spark-2.2.1-bin-hadoop2.7")`
To run full program use `python readList.py`<br />
Output will be printed to a JSON file<br />
