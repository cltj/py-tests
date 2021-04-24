# NOT DONE

# pip install requests

import os
import requests

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
self.account_name = os.getenv("TABLES_STORAGE_ACCOUNT_NAME")

print(storageAccount)

"""
filter = "balance gt '2000.40'"
select = "id, balance"
sig = "Z9NUFLu5GrlC%2Brj2eV17WKqXvL1iAs24YbG7gG7gpFQ%3D"

url = u"https://" + storageAccount + ".table.core.windows.net/accounts?sv=2020-02-10&ss=t&srt=sco&sp=rwdlacu&se=2022-04-12T17:58:45Z&st=2021-04-12T09:58:45Z&spr=https&sig=" + sig + "&$select=" + select + "&$filter="+ filter

payload={}
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json'
}

response1 = requests.request("GET", url, headers=headers, data=payload)

print(response1.text)
"""