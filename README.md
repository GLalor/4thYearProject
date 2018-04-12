# 4thYearProject
College 4th/Final year project 

## Requirements 
   - Nvidia Cuda libraries and tools
   - Pycuda
   - Numpy
   - Beatifulsoup library
   - Spark
   - Hadoop
   - Findspark (python lib)<br />
   (I am running Spark 2.2.1 and Hadoop 2.7.5)
   
## TO RUN MASTER branch
To run full program use `python startCalculation.py` <br />
Please see sample output below: <br />

![alt text](https://github.com/GLalor/Vanilla-Option-Pricer/blob/master/Images/output.PNG "Sample output")


## TO RUN MULTIPROSS branch
Run code on machine with **NVidia GPU installed**<br />
To run full program use `python startCalculation.py`<br />
You will need to comment out the standard calculation and uncomment the gpu calculation calls<br />
Output will be printed to a JSON file<br />

## TO RUN SPARK branch
Run code on machine with **Spark, Hadoop and findspark installed**<br />
User will first need to modify Line 6 to point to there installation of spark<br />
   `findspark.init("C:\spark-2.2.1-bin-hadoop2.7")`<br />
To run full program use `python startCalculationSpark.py`<br />
Output will be printed to a JSON file<br />

## PLEASE NOTE
Hadoop is directed to write to a directory called `ProjectDB` <br />
I store this on a drive `E:` the code to change this is in <br />
Please change these two lines if needed to change the storage location <br />
`option_prices_data.write.save('E:\ProjectDB', format='json', mode='append')` <br />
`resultsHiveDF = sparkSession.read.format('json').load('E:\ProjectDB')` <br />
