import os
import sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.constants.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS
    )
from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.utils.utils import save_numpy_array,save_pickle

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            logging.info("Reading data")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformation_obj(cls)->Pipeline:
        try:
            logging.info("Creating data transformation pipeline")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            return Pipeline([('imputer',imputer)])
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Initiating data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #trainig data
            train_target = train_df[TARGET_COLUMN]
            train_features = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target = train_target.replace(-1,0)

            #testing data
            test_target = test_df[TARGET_COLUMN]
            test_features = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target = test_target.replace(-1,0)

            preprocessor = self.get_data_transformation_obj()
            preprocrssor_obj = preprocessor.fit(train_features)
            train_features_transformed = preprocrssor_obj.transform(train_features)
            test_features_transformed = preprocessor.transform(test_features)

            train_arr = np.c_[train_features_transformed,np.array(train_target)]
            test_arr = np.c_[test_features_transformed,np.array(test_target)]

            save_numpy_array(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_pickle(self.data_transformation_config.transformed_object_file_path,preprocrssor_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path
            )

            return data_transformation_artifact
 
        except Exception as e:
            raise NetworkSecurityException(e, sys)