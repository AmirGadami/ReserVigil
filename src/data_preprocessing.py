
import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from config.path_config import *
from src.custom_exception import CustomException
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)


class DataProcessor:

    def __init__(self,train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info('Starting our Data Processing Step')

            logger.info('Dropping the columns')
            df.drop(columns=["Unnamed: 0","Booking_ID"],inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Label encoding")

            label_encoder = LabelEncoder()

            mappings = {}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col]= {label:code for label,code in zip(label_encoder.classes_,label_encoder.transform(label_encoder.classes_))}
            logger.info("Label Mapping are : ")
            for col,mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            
            logger.info("Doing Skewness Handling")

            skew_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x:x.skew())

            for column in skewness[skewness>skew_threshold].index:
                df[column] = np.log1p(df[column])
                
            return df

        except Exception as e:
            logger.error("Error during Skewing Data ,{e}")
            raise CustomException('Error while Skewing data',e)
        
    def balanced_data(self, df):
        try:
            logger.info('Handling inbalanced Data')

            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            x_resample, y_resample = smote.fit_resample(X,y)

            balanced_df = pd.DataFrame(x_resample,columns=X.columns)
            balanced_df['booking_status'] = y_resample

            logger.info('Data balanced Successfully')

            return balanced_df
        except Exception as e:
            logger.error(f'Error during balancing data step {e}')
            raise CustomException('error while balancing data',e)
            
        
    def select_features(self,df):
        try:
            logger.info('Starting out feature selection step')


            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({'feature': X.columns,
                'importance': feature_importance
                                })
            
            top_features = feature_importance_df.sort_values(by='importance',ascending=False)
            num_features_to_select = self.config['data_processing']['no_of_features']
            logger.info(f"feature selected: {num_features_to_select}")


            top_10_features = top_features['feature'].head(num_features_to_select).values
            top_10_df = df[top_10_features.tolist()+ ['booking_status']]

            logger.info('feature selection completed successfully')

            return top_10_df
        
        except Exception as e:
            logger.error(f'Error during feature selection data step {e}')
            raise CustomException('error while feature selection',e)
        

    def save_data(self, df, file_path):
        try:

            logger.info('Saving data into processed folder')

            df.to_csv(file_path, index=False)

            logger.info(f"Data saved successfully to {file_path}")

        except Exception as e:
            logger.error(f'Error during saving data step {e}')
            raise CustomException('error while saving',e)
        

    def process(self):
        try:
            logger.info('Loading data from RAM directory')

            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)

            train_data = self.preprocess_data(train_data)
            test_data = self.preprocess_data(test_data)

            train_data = self.balanced_data(train_data)
            test_data = self.balanced_data(test_data)

            train_data = self.select_features(train_data)
            test_data = test_data[train_data.columns]

            self.save_data(train_data,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_data, PROCESSED_TEST_DATA_PATH)

            logger.info('Processed data completed successfully')

        except Exception as e:
            logger.error('Error during Processing Pipeline')
            raise CustomException('error while Processing Pipelineing',e)
        


if __name__ == "__main__":

    processor = DataProcessor(TRAIN_PATH,TEST_PATH,PROCESSED_DIR, CONFIG_PATH)
    processor.process()
