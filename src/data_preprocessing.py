
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
            skew_threshold = self.config['data_preprocessing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x:x.skew())
        except:
            pass


