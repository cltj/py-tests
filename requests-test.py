# NOT DONE

# pip install requests

import requests, os, string
from dotenv import find_dotenv, load_dotenv
from twilio.rest import Client

#Def
load_dotenv(find_dotenv())
account_name = os.getenv("STORAGE_ACCOUNT_NAME")
sig = os.getenv("SIG")
tibberKey = os.getenv("TIBBER_ACCESS_KEY")
tibberHomeId = os.getenv("TIBBER_HOME_ID")


twil_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twil_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twil_client = Client(twil_account_sid, twil_auth_token)

twil_new_key = twil_client.new_keys.create()

print(twil_new_key.sid)




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





print("##########  Response from azure tables ###########")
print(response1.text)

print("##########  Response from tibber ###########")
print(response2.text)
