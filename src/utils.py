# src/utils.py
import os
import pickle
import sys
import numpy as np
import pandas as pd

# Import custom exception
from src.exception import CustomException

def save_object(file_path, object):
    """
    Saves a Python object to a pickle file.
    Creates directory if it doesn't exist.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            pickle.dump(object, file_obj)
            
    except Exception as e:
        raise CustomException(e)