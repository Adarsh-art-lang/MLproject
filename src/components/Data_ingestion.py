import os
import sys
from dataclasses import dataclass

# Importing logging and custom exception from your project structure
from src.logger import logging
from src.exception import CustomException

import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass
class DataIngestionConfig:
    """
    Configuration class to store paths for data ingestion.
    Using @dataclass allows defining variables directly without __init__.
    """
    # Path where raw data will be saved
    raw_data_path: str = os.path.join('artifact', 'raw.csv')
    
    # Path where training data will be saved
    train_data_path: str = os.path.join('artifact', 'train.csv')
    
    # Path where test data will be saved
    test_data_path: str = os.path.join('artifact', 'test.csv')


class DataIngestion:
    """
    Class to handle the data ingestion process.
    Includes methods to read data, split it, and save to specific paths.
    """
    
    def __init__(self):
        """
        Initialize the DataIngestion class with configuration.
        self.ingestion_config holds the path configurations.
        """
        self.ingestion_config = DataIngestionConfig()
        logging.info("DataIngestion object initialized with configuration paths.")

    def initiate_data_ingestion(self):
        """
        Main method to initiate the data ingestion pipeline.
        Steps:
        1. Read the dataset.
        2. Create necessary directories.
        3. Save raw data.
        4. Split data into train and test.
        5. Save train and test data.
        6. Return paths for the next stage (Data Transformation).
        """
        logging.info("Entered the data ingestion method or component")
        
        try:
            # 1. Read the dataset
            # Assuming the raw data is in 'notebook/data/student.csv'
            # Adjust this path if your data source changes (e.g., MongoDB, API)
            df = pd.read_csv('Notebook/Data/stud.csv')
            
            logging.info("Read the dataset as DataFrame")
            
            # 2. Create directories if they don't exist
            # The parent directory (e.g., 'artifact') is extracted from the config paths
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # 3. Save the raw data to the configured raw_data_path
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Saved raw data to CSV")
            
            # 4. Split the data into Train and Test sets
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(
                df, 
                test_size=0.2, 
                random_state=42
            )
            
            # 5. Save the split data to their respective paths
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            logging.info("Ingestion of the data is completed")
            
            # 6. Return the paths for the next stage (Data Transformation)
            return (
                self.ingestion_config.raw_data_path,
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            logging.info("Exception occurred in data ingestion")
            # Raise custom exception with error details
            raise CustomException(e, sys)


if __name__ == "__main__":
    # Entry point to run the data ingestion pipeline
    obj = DataIngestion()
    obj.initiate_data_ingestion()