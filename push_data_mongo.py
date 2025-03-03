from dotenv import load_dotenv
import os
import sys
import json
load_dotenv()
from collections.abc import MutableMapping


MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()  # Get the location of the Certified Authority file

import pandas as pd
import pymongo
import numpy as np
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging


class PushDataMongo:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def push_data(self,records,collection_name,database_name):
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = database_name
            self.collection = collection_name
            self.records = records
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    try:
        DATABASE = "NetworkSecurity"
        Collection = "NetworkSecurityData"
        file_path = "Network_Data\phisingData.csv"
        push_data_obj = PushDataMongo()
        records = push_data_obj.csv_to_json(file_path)
        no_of_records = push_data_obj.push_data(records,Collection,DATABASE)
        print(f"Number of records inserted: {no_of_records}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)