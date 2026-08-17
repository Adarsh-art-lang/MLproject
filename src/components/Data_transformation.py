# src/components/data_transformation/transformer.py
import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Importing custom exception and logger
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
#from src.components.Data_transformation import DataTransformationConfig

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join(
        'artifacts',
        'preprocessor.pkl'
    )

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig):
        self.data_transformation_config = data_transformation_config

    def get_transformer_object(self):
        """
        Returns the ColumnTransformer object containing pipelines for 
        numerical and categorical columns.
        """
        try:
            logging.info("Start of get_transformer_object")
            
            # Defining Numerical and Categorical Columns
            # These were identified during EDA in previous videos
            numerical_columns = ["writing_scores", "reading_scores"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            # Pipeline for Numerical Columns
            # Step 1: Impute missing values using Median (to handle outliers)
            # Step 2: Standard Scale
            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # Pipeline for Categorical Columns
            # Step 1: Impute missing values using Most Frequent
            # Step 2: One Hot Encoding
            # Step 3: Standard Scale (as shown in the video)
            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler())
                ]
            )

            logging.info("Categorical columns encoding completed")
            logging.info("Numerical columns scaling completed")

            # Combine both pipelines using ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", numerical_pipeline, numerical_columns),
                    ("categorical_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            logging.info("Preprocessor object created successfully")
            return preprocessor

        except Exception as e:
            raise CustomException(e)

    def initiate_data_transformation(self, train_path, test_path):
        """
        Main method to execute data transformation.
        Reads train/test data, applies transformation, and saves the preprocessor.
        """
        try:
            logging.info("Start of initiate_data_transformation")

            # 1. Read Training and Test Data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and Test data read completed")

            # 2. Obtain Preprocessor Object
            logging.info("Obtaining pre-processing object")
            preprocessor = self.get_transformer_object()

            # 3. Define Target Column
            target_column_name = "math_score"

            # 4. Drop Target Column from Input Features
            # Note: The speaker explicitly used axis=1 here to drop columns
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)

            target_feature_train_df = train_df[[target_column_name]]
            target_feature_test_df = test_df[[target_column_name]]

            logging.info("Applying transform on train and test data")

            # 5. Fit and Transform
            # Fit on train, Transform on both
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # Convert arrays to DataFrame (Optional, but good for inspection)
            # The speaker kept them as arrays in the return, but the logic is clear.
            
            # 6. Save the Preprocessor Object
            logging.info("Saving preprocessor object")
            file_path = self.data_transformation_config.preprocessor_obj_file_path
            
            save_object(
                file_path=file_path,
                object=preprocessor
            )

            logging.info("Preprocessor saved successfully")

            return (
                input_feature_train_arr,
                target_feature_train_df,
                input_feature_test_arr,
                target_feature_test_df,
                preprocessor
            )

        except Exception as e:
            raise CustomException(e)