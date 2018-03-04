import json
import optionCalculation
import time
import getSNPList
import optionCalculationGPU

def main():
    start_time = time.time()
    printDescription()
    data = getSNPList.main()
    for item in data['members']:
            # for testing purposes if item['sym'] == "AAPL":
        print(item['sym'])
        #optionCalculation.main(item['sym'])
        optionCalculationGPU.main(item['sym'])
    print("******** finsihed in %s seconds ********" %
          (time.time() - start_time))


def printDescription():
    print("Program to print ticker symbols of stocks in S and P 500 list")


# Stops code being run on import
if __name__ == "__main__":
    main()