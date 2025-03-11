import os,sys
import numpy as np
import dill
import yaml
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array(file_path: str, data: np.ndarray) :
    try:
        dir_path =os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, data)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_pickle(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_pickle(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"File not found at {file_path}", sys)
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array(file_path: str) -> np.ndarray:
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(f"File not found at {file_path}", sys)
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)