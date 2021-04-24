import os, uuid, string, random
from dotenv import find_dotenv, load_dotenv

class accountTable(object):

    def __init__(self):
        load_dotenv(find_dotenv())
        self.connection_string = os.getenv("AZURE_TABLES_CONNECTION_STRING")
        self.access_key = os.getenv("TABLES_PRIMARY_STORAGE_ACCOUNT_KEY")
        self.endpoint = os.getenv("TABLES_STORAGE_ENDPOINT_SUFFIX")
        self.account_name = os.getenv("TABLES_STORAGE_ACCOUNT_NAME")
        self.account_url = "{}.table.{}".format(self.account_name, self.endpoint)
        self.connection_string = u"DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
            self.account_name,
            self.access_key,
            self.endpoint
        )
        self.table_name = "accounts"
        newAccountId = uuid.uuid4()

        def random_char(y):
            return ''.join(random.choice(string.ascii_uppercase) for x in range(y))
        newRowKey = random_char(6)

        self.entity = {  
            "balance":0.00,
            "customerId@odata.type":"Edm.Guid",
            "customerId":"",
            "id@odata.type":"Edm.Guid",
            "id":newAccountId,
            "currency":"usd",
            "PartitionKey":"9876543210",
            "RowKey":newRowKey,
        }

    def create_entity(self):
        from azure.data.tables import TableClient
        from azure.core.exceptions import ResourceExistsError, HttpResponseError

        with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:
            try:
                entity = table_client.create_entity(entity=self.entity)
                return(self.entity)
            except ResourceExistsError:
                print("Entity already exists")


    def query_entity(self, id):
        from azure.data.tables import TableClient
        from azure.core.exceptions import HttpResponseError

        with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:
            try:
                parameters = {
                    "id": id
                }
                name_filter = "id eq @id" 
                #name_filter = u"id eq guid'97294d5e-5122-4aa5-819a-1edaa1b11e33'" # guid example
                #name_filter = u"Timestamp ge datetime'2021-04-16T15:00:00.000Z'" # Timestamp example
                #name_filter = u"IsActive eq true" # Boolean example
                # https://docs.microsoft.com/en-us/samples/azure/azure-sdk-for-python/tables-samples/ 
                queried_entities = table_client.query_entities(
                    filter=name_filter, select=[u"balance",u"PartitionKey",u"RowKey",u"currency",u"id",u"customerId"], parameters=parameters)
                for entity_chosen in queried_entities:
                    return (entity_chosen)
            except HttpResponseError as e:
                print(e.message)


    def update_entity(self, id, amount):
        from azure.data.tables import TableClient, UpdateMode

        with TableClient.from_connection_string(self.connection_string, self.table_name) as table_client:
            try:
                parameters = {
                    "id": id
                }
                name_filter = "id eq @id" 
                #name_filter = u"id eq guid'279cdc13-ff2e-4ebf-88bd-faccdb0015f9'"
                get_entity = table_client.query_entities(filter=name_filter, parameters=parameters)

                for entity_chosen in get_entity:
#                    print(entity_chosen)

                # Merge the entity
                    entity_chosen.balance = amount
                    table_client.update_entity(mode=UpdateMode.MERGE, entity=entity_chosen)

                # Get the merged entity
                    merged = table_client.get_entity(partition_key=entity_chosen.PartitionKey, row_key=entity_chosen.RowKey)
                    #print("SUCCESSFUL MERGED ENTITY: {}".format(merged))
                    return (entity_chosen)

            except HttpResponseError as e:
                print(e.message)


    def delete_entity(self, id):
        from azure.data.tables import TableClient
        from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError
        from azure.core import MatchConditions

        with TableClient(account_url=self.account_url, credential=self.access_key, table_name=self.table_name) as table_client:
            try:
                parameters = {
                    "id": id
                }
                name_filter = "id eq @id" 
                #name_filter = u"id eq guid'a1f4d007-3201-4c0c-a669-655443a8f506'"
                get_entity = table_client.query_entities(filter=name_filter, parameters=parameters)

                for entity_chosen in get_entity:
                    table_client.delete_entity(
                    row_key=entity_chosen.RowKey,
                    partition_key=entity_chosen.PartitionKey
                )
                    return (entity_chosen)
            except ResourceNotFoundError:
                print("Entity does not exists")




#print(accountTable().create_entity())
#print(accountTable().query_entity())
#print(accountTable().update_entity())
#print(accountTable().delete_entity())
amount = 1030.33
newAccountGuid = accountTable().create_entity()
newGuid = newAccountGuid['id']
newRow = newAccountGuid['RowKey']
print(newRow + " created...")
print("--------------------------------------")
queryNewAccount = accountTable().query_entity(newGuid)
newQuery = queryNewAccount['RowKey']
queryBalance = queryNewAccount['balance']
print(newQuery + " queried, and balance is " + str(queryBalance) + " ...")
print("--------------------------------------")
updateNewAccount = accountTable().update_entity(newGuid,amount)
newBalance = updateNewAccount['balance']
print(newQuery + " updated balance is " + str(newBalance) + " ...")
print("--------------------------------------")
deleteNewAccount = accountTable().delete_entity(newGuid)
print(deleteNewAccount['RowKey'] + " is successfully deleted...")
