import os
import sys
from dataclasses import dataclass

from src.logger import logging 
from src.exception import CustomException
import pandas as pd
import numpy as np

from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

@dataclass()
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join("artifacts", "preprecessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformation()

    def get_data_transformation_object(self):
        try:
            logging.info("data transformation initiated")

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = X.select_dtypes(include='object').columns
            numerical_cols = X.select_dtypes(exclude='object').columns

            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info("Pipeline Initiated")

            ## Numerical Pipeline
            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())

                ]

            )

            # Categorigal Pipeline
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaler',StandardScaler())
                ]

            )

           

            preprocessor=ColumnTransformer([
            ('num_pipeline',num_pipeline,numerical_cols),
            ('cat_pipeline',cat_pipeline,categorical_cols)
            ])

            return preprocessor

            logging.info("Pipeline Completed")


        except Exception as e:
            logging.info("error occured at data transformation stage")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            #Reading train and test data
            train_df= pd.read_csv(train_path)
            test_df= pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info(f"train data head:\n{train_df.head().to_string()}")
            logging.info(f"test data head: \n {test_df.head().to_string()}")

            logging.info("Obtaining a preprocessing object")

            preprocessing_obj= self.get_data_transformation_object()

            target_column_name= "price"
            drop_columns= [target_column_name, "id"]

            input_feature_train_df= train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df= train_df[target_column_name]

            input_feature_test_df= test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df= test_df[target_column_name]


            #Transformation using preprocessor_obj
            input_feature_train_arr= preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr= preprocessing_obj.transform(input_feature_test_df)
            logging.info("Applying preprocessing object on training and testing datasets")

            train_arr= np.c_(input_feature_train_arr, np.array(target_feature_train_df))
            test_arr= np.c_(input_feature_test_arr, np.array(target_feature_test_df))


            
        except Exception as e:
            logging.info("Error occured in initiate_data_transformation")
            raise CustomException(e, sys)

