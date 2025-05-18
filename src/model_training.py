
import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from config.model_params import *
from utils.common_functions import  read_yaml, load_data
from scipy.stats import randint

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f'fLoading data from {self.train_path}')
            train_df = load_data(self.train_path)
        
            logger.info(f'fLoading data from {self.test_path}')
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']

            logger.info('Data splitted successfully for model training')

            return X_train,y_train,X_test,y_test
        
    
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException('Failed to load data',e)
            
    def train_lgbm(self,X_train,y_train):
        try:
            logger.info('Initializing our model')
            lgbm_model = lgb.LGBMClassifier(random_state = self.random_search_params['random_state'])

            logger.info("Starting our hyperparameter tuning")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv = self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state = self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring'],  
            )

            logger.info('Starting our Hyperparameter tuning')

            random_search.fit(X_train,y_train)

            logger.info('Hyperparameter tuning is Done')

            best_parameters = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f'Best parameters are: {best_parameters}' ) 

            return best_lgbm_model

        except Exception as e:
            logger.error(f"Error while Training Model {e}")
            raise CustomException('Failed to Training model',e)
        

            
    def evaluate_model(self,model, X_test, y_test):
        try:
            logger.info('Evaluating Model')

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f'accuracy score: {accuracy}')
            logger.info(f'recall: {recall}')
            logger.info(f'Preciion: {precision}')
            logger.info(f'F1: {f1}')
            return {
                'accuracy' :accuracy,
                'recall' : recall,
                'precision':precision,
                'f1':f1
            }
        except Exception as e:
            logger.error(f"Error while getting the Scores {e}")
            raise CustomException('Failed to get the scores',e)
        
    def save_mode(self,model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok=True)

            logger.info('saving the model')

            joblib.dump(model,self.model_output_path)
            logger.info('Model saved to the path')

        except Exception as e:
            logger.error(f"Error while save Model {e}")
            raise CustomException('Failed to save model',e)
        
    def run(self):
        try:
            logger.info('Starting our model training Pipline')
            
            X_train,y_train,X_test,y_test = self.load_and_split_data()

            best_lgbm_model = self.train_lgbm(X_train,y_train)

            metrics = self.evaluate_model(best_lgbm_model, X_test,y_test)
            self.save_mode(best_lgbm_model)

            logger.info('Model Training Successfully Completed')
        
        except Exception as e:
            logger.error(f"Error while doing the pipeline {e}")
            raise CustomException('Failed in Pipeline',e)
        
if __name__ == "__main__":

    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,
                            PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT)
    trainer.run()