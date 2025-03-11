
from sklearn.metrics import r2_score
from NetworkSecurity.entity.artifact_entity import ModelClassificationArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
from NetworkSecurity.Exception.exception import NetworkSecurityException
import sys
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from sklearn.model_selection import GridSearchCV

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)


def get_classification_details(y_true,y_pred)->ModelClassificationArtifact:
    try:
            
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric =  ModelClassificationArtifact(f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)