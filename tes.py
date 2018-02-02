import json
data = json.load(open('optionPrices.json'))

maxPrice = 0 
result = "The best Call price for MMM is "
print(data['MMM']['Put'])
# for item in data['MMM']['Put']:
#     print(item.getValue())