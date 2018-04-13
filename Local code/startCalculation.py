import json
import optionCalculation
import time
import getSNPList
import riskRateRetrieval
import optionCalculationGPU


def main():
    start_time = time.time()
    printDescription()
    data = getSNPList.main()
    rates = riskRateRetrieval.main()
    for item in data['members']:
        print(item['sym'])
        # optionCalculation.main(item['sym'], rates) # Calculates using CPU
        optionCalculationGPU.main(item['sym'], rates)  # Calculates using GPU
    print("******** finsihed in %s seconds ********" %
          (time.time() - start_time))


def printDescription():
    print("Program to calculate option prices for each company in S and P 500 list based of data retrieved from a Yahoo api")


# Stops code being run on import
if __name__ == "__main__":
    main()
