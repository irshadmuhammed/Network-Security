from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact
from NetworkSecurity.logging.logger import logging
import os
import pymongo
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import List
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            self.config = config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_to_dataframe(self):  
        try:
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            db_name = self.config.database_name
            collection_name = self.config.collection_name
            collection = self.client[db_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1) 
            
            df.replace({"na": np.nan}, inplace=True)  
            return df  
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_feature_store(self, dataframe: pd.DataFrame):
        try:
            dir_path = os.path.dirname(self.config.feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(self.config.feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_test_split_data(self, dataframe: pd.DataFrame):
        try:
            train_df, test_df = train_test_split(dataframe, test_size=self.config.train_test_split_ratio)
            dir_path = os.path.dirname(self.config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Train test split is done")
            train_df.to_csv(self.config.training_file_path, index=False, header=True)
            test_df.to_csv(self.config.testing_file_path, index=False, header=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_to_dataframe() 
            dataframe = self.export_data_feature_store(dataframe)
            self.train_test_split_data(dataframe)  
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.config.training_file_path,
                testing_file_path=self.config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
