from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from NetworkSecurity.components.data_validation import DataValidation
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
        print(data_ingestion_Artifact)
        logging.info("Data Ingestion completed")

        logging.info("Data validation strated")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validataion = DataValidation(data_ingestion_Artifact,data_validation_config)
        data_validation_artifact = data_validataion.initiate_data_validation()
        logging.info("Data validation initiated")
        print(data_validation_artifact)
        logging.info("Data validation completed")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)