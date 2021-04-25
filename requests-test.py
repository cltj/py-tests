# NOT DONE

# pip install requests

import requests, os, string, json
from dotenv import find_dotenv, load_dotenv


#Def
load_dotenv(find_dotenv())
account_name = os.getenv("STORAGE_ACCOUNT_NAME")
sig = os.getenv("SIG")
tibberKey = os.getenv("TIBBER_ACCESS_KEY")
tibberHomeId = os.getenv("TIBBER_HOME_ID")


# Query azure tables with SAS key
filter = "balance gt '2000.40'"
select = "id, balance"

url = f"https://" + account_name + ".table.core.windows.net/accounts?sv=2020-02-10&ss=t&srt=sco&sp=rwdlacu&se=2022-04-12T17:58:45Z&st=2021-04-12T09:58:45Z&spr=https&sig=" + sig + "&$select=" + select + "&$filter="+ filter

payload={}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

# Response azure table
response1 = requests.request("GET", url, headers=headers, data=payload)


# Query tibber for energy price
url = "https://api.tibber.com/v1-beta/gql"

payload="{\"query\":\"{\\n  viewer {\\n    homes {\\n      currentSubscription{\\n        priceInfo{\\n          current{\\n            total\\n            energy\\n            tax\\n            startsAt\\n          }\\n          today {\\n            total\\n            energy\\n            tax\\n            startsAt\\n          }\\n          tomorrow {\\n            total\\n            energy\\n            tax\\n            startsAt\\n          }\\n        }\\n      }\\n    }\\n  }\\n}\\n\\n\",\"variables\":{}}"
headers = {
  'Authorization': 'Bearer ' + tibberKey ,
  'Content-Type': 'application/json'
}

response2 = requests.request("POST", url, headers=headers, data=payload)

# Do some ops on return data
json_string = response2.text
obj = json.loads(json_string)
today = obj["data"]["viewer"]["homes"][0]["currentSubscription"]["priceInfo"]["today"]
dailyTax = 0
dailyPrice = 0
i = len(today)

for i in range(i):
    total = today[i]["total"]
    tax = today[i]["tax"]
    dailyTax += tax
    dailyPrice += total
#    print("Total: " + str(total) + ", Tax: " + str(tax))
avgPrice = round(dailyPrice/24,3)
avgTax = round(dailyTax/24,3)
avgTaxPc = round(avgTax/avgPrice*100,1) 


# Query tibber about consumption

url1 = "https://api.tibber.com/v1-beta/gql"

payload1="{\"query\":\"{\\n  viewer {\\n    homes {\\n      timeZone\\n      address {\\n        address1\\n        postalCode\\n        city\\n      }\\n      owner {\\n        firstName\\n        lastName\\n        contactInfo {\\n          email\\n          mobile\\n        }\\n      }\\n      consumption(resolution: HOURLY, last: 24) {\\n        nodes {\\n          from\\n          to\\n          cost\\n          unitPrice\\n          unitPriceVAT\\n          consumption\\n          consumptionUnit\\n        }\\n      }\\n      currentSubscription {\\n        status\\n        priceInfo {\\n          current {\\n            total\\n            energy\\n            tax\\n            startsAt\\n          }\\n        }\\n      }\\n    }\\n  }\\n}\\n\\n\",\"variables\":{}}"
headers1 = {
  'Authorization': 'Bearer ' + tibberKey,
  'Content-Type': 'application/json'
}

response3 = requests.request("POST", url1, headers=headers1, data=payload1)

# Do some ops on return consumption data
json_string1 = response3.text
obj1 = json.loads(json_string1)
nodes = obj1["data"]["viewer"]["homes"][0]["consumption"]["nodes"]

dailyCost = 0
dailyUnitPrice = 0
dailyUnitPriceVAT = 0
dailyConsumption = 0
n = len(nodes)

for n in range(n):
    cost = nodes[n]["cost"]
    unitPrice = nodes[n]["unitPrice"]
    unitPriceVAT = nodes[n]["unitPriceVAT"]
    consumption = nodes[n]["consumption"]
    if consumption is None:
      consumption = 0.0
      cost = 0.0
    dailyCost += cost 
    dailyUnitPrice += unitPrice
    dailyUnitPriceVAT += unitPriceVAT
    dailyConsumption += consumption

avgCost = round(dailyCost/24,3)
avgUnitPrice = round(dailyUnitPrice/24,3)
avgUnitPriceVAT = round(dailyUnitPriceVAT/24,3)
avgConsumption = round(dailyConsumption/24,3) 

totCost = round(dailyCost,3)
totUnitPrice = round(dailyUnitPrice,3)
totUnitPriceVAT = round(dailyUnitPriceVAT,3)
totConsumption = round(dailyConsumption,3) 




# PRINTS #
print("##########  Response from azure tables ###########")
print(response1.text)
print("##########  Response from tibber ###########")
print("----------------  Energy Prices  --------------------")
print("Todays average electricity price was " + str(avgPrice) + " nok , where " + str(avgTax) + " nok (" + str(avgTaxPc) + "%)" + " was taxes")
print("------------------  CONSUMPTION  --------------------")
print("Todays AVERAGE electricity numbers:\n        cost: " + str(avgCost) + " NOK \n        unit price: " + str(avgUnitPrice) + " NOK \n        unitVAT: " + str(avgUnitPriceVAT) + " NOK \n        consumption: " + str(avgConsumption) + " KWH\n\n" )
print("Todays TOTAL electricity numbers:\n        totalCost: " + str(totCost) + " NOK \n        unit price: " + str(totUnitPrice) + " NOK \n        unitVAT: " + str(totUnitPriceVAT) + " NOK \n        consumption: " + str(totConsumption) + " KWH\n\n")
