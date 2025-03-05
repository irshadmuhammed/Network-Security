from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
import sys


if __name__ == "__main__":
    try:
        logging.info("Data Ingestion started")
        training_pipeline_config = TrainingPipelineConfig()
        config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(config)
        data_ingestion_Artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")

        print(data_ingestion_Artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)