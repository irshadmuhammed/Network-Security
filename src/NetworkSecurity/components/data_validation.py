from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.logging.logger import logging
import pandas as pd
import os,sys
from scipy.stats import ks_2samp

from NetworkSecurity.utils.utils import read_yaml,write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def check_schema_colums(self, dataframe: pd.DataFrame):
        try:
            no_of_columns_schema = len(self._schema_config)
            logging.info(f"Schema columns: {no_of_columns_schema}")
            logging.info(f"Dataframe columns: {len(dataframe.columns)}")

            if no_of_columns_schema == len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def check_numeric_columns(self, dataframe: pd.DataFrame):
        try:
            numeric_columns = dataframe.select_dtypes(include=['int64', 'float64']).columns.tolist()
            logging.info(f"Numeric columns: {numeric_columns}")
            numeric_columns_schema = self._schema_config['numerical_columns']
            logging.info(f"Numeric columns schema: {numeric_columns_schema}")

            missing_columns = [col for col in numeric_columns_schema if col not in numeric_columns]

            if missing_columns:
                return True
            return False

            if set(numeric_columns) == set(numeric_columns_schema):
                return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def detect_drift(self,base_df,current_df,threshold=0.05):
        try:
            status= True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })

                drift_file_path = self.data_validation_config.drift_report_file_path
                dir = os.path.dirname(drift_file_path)
                os.makedirs(dir,exist_ok=True)

                write_yaml_file(file_path=drift_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self):
        try:
            train_file_Path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path

            train_dataframe = DataValidation.read_data(train_file_Path)
            test_dataframe = DataValidation.read_data(test_file_path)

            status = self.check_schema_colums(train_dataframe)
            if not status:
                error_message = f"Schema columns are not matching train dataframe"

            status = self.check_schema_colums(test_dataframe)
            if not status:
                error_message = f"Schema columns are not matching test dataframe"

            status  = self.check_numeric_columns(train_dataframe)
            if status:
                error_message = f"Numeric columns are not matching train dataframe"

            status  = self.check_numeric_columns(test_dataframe)
            if status:
                error_message = f"Numeric columns are not matching test dataframe"

            status = self.detect_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,header=True,index=False
            )
            
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.testing_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)