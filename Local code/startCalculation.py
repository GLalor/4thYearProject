import json
import optionCalculation
import time
import getSNPList
import riskRateRetrieval
import optionCalculationGPU
import writeToHDFS

def main():
    start_time = time.time()
    printDescription()
    data = getSNPList.main()
    rates = riskRateRetrieval.main()
    for item in data['members']:
        print(item['sym'])
        optionCalculation.main(item['sym'], rates)
    writeToHDFS.writeResultHive()
    print("******** finsihed in %s seconds ********" %
          (time.time() - start_time))


def printDescription():
    print("Program to print ticker symbols of stocks in S and P 500 list")


# Stops code being run on import
if __name__ == "__main__":
    main()