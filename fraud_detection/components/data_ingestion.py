from fraud_detection.entity.config_entity import DataIngestionConfig
import os, sys
from fraud_detection.exception import AppException
from fraud_detection.logger import logging
from fraud_detection.constant import *
from fraud_detection.entity.artifact_entity import DataIngestionArtifact
import tarfile
import numpy as np
from six.moves import urllib
import shutil
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion log started{'>>'*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise AppException (e,sys) from e
        
    
    def download_frauddetection_data(self,) -> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir, exist_ok= True)

            file_name = FILE_NAME

            raw_data_file_path = os.path.join(raw_data_dir, file_name)

            logging.info(f"Downloading file from: [{download_url}] into: [{raw_data_file_path}]")

            urllib.request.urlretrieve(download_url, raw_data_file_path)

            logging.info(f"File: [{raw_data_file_path}] has been downloaded successfully")

            return raw_data_file_path
        
        except Exception as e:
            raise AppException(e,sys) from e
        

    def split_data_train_test(self, raw_data_file_path) -> DataIngestionArtifact:
        
        try:

            file_path = raw_data_file_path

            logging.info(f"Reading csv file: [{file_path}]")
            data_frame = pd.read_csv(file_path)

            fraud_df = data_frame.loc[data_frame['isFraud'] == 1]
            non_fraud_df = data_frame[data_frame['isFraud'] == 0][:len(fraud_df)]

            data_frame = pd.concat([fraud_df, non_fraud_df])
            data_frame.reset_index(drop=True, inplace=True)

            data_frame["cat_amount"] = pd.cut(data_frame["amount"], 4, labels=[1,2,3,4])

            logging.info(f"Splitting data into train and test")

            strat_train_set = None
            strat_test_set = None

            strat_shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in strat_shuffle_split(data_frame, data_frame["cat_amount"]):
                strat_train_set = data_frame.loc[train_index].drop(["cat_amount"], axis=1)
                strat_test_set = data_frame.loc[test_index].drop(["cat_amount"], axis=1)

                train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, FILE_NAME)
                test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, FILE_NAME)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training data to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting training data to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path, test_file_path=test_file_path,
                                                            isingested=True, 
                                                            message=f"Data Ingestion completed successfully")

            logging.info(f"Data Ingestion Artifact: [{data_ingestion_artifact}]")

            return data_ingestion_artifact
    
        except Exception as e:
            raise AppException(e,sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            raw_data_file_path = self.download_frauddetection_data()
            return self.split_data_train_test(raw_data_file_path)
        except Exception as e:
            raise AppException(e,sys) from e
        
        









