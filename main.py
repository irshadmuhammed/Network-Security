from NetworkSecurity.components.model_trainer import ModelTrainer
from NetworkSecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig,DataValidationConfig, ModelTrainingConfig
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
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

        logging.info("Data transformation started")
        data_transfromation_config = DataTransformationConfig(training_pipeline_config)
        data_transfromation = DataTransformation(data_validation_artifact,data_transfromation_config)
        data_transformation_artifact = data_transfromation.initiate_data_transformation()
        logging.info("Data transformation initiated")
        print(data_transformation_artifact)
        logging.info("Data transformation completed") 

        logging.info("Model training started") 
        model_training_config = ModelTrainingConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_training_config,data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed") 
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)