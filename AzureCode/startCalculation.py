import json
import optionCalculation
import time
import getSNPList
import riskRateRetrieval
import optionCalculationGPU
import deleteOldBlobsFiles


def main():
    start_time = time.time()
    deleteOldBlobsFiles.main()
    printDescription()
    data = getSNPList.main()
    rates = riskRateRetrieval.main()
    for item in data['members']:
        print(item['sym'])
        optionCalculationGPU.main(item['sym'], rates)
    print("******** finsihed in %s seconds ********" %
          (time.time() - start_time))


def printDescription():
    print("Program to calculate option prices for each company in S and P 500 list based of data retrieved from a Yahoo api")


# Stops code being run on import
if __name__ == "__main__":
    main()
