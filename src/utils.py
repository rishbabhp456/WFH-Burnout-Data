import os
import sys

# Add root directory to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_data_collection
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import json
import numpy as np
import pandas as pd
import pickle
import config

class WFH_Burnout:
    def __init__(self):
        pass

    def load_model(self):
        """"
        This function is to load the model
        """
        self.model = tf.keras.models.load_model(config.MODEL_PATH)
        return self.model
    
    def load_column_data(self):
        """"
        This function is to load the json file
        """
        with open(config.COLUMN_DATA_PATH,'r') as f:
            self.input_columns = json.load(f)
        return self.input_columns
    
    def load_std_scalar(self):
        """"
        This function is to load the std scalar file
        """
        with open(config.STD_SCALAR_PATH,'rb') as s:
            self.std_scalar = pickle.load(s)
        return self.std_scalar
    
    def create_input(self):
        """"
        This function is to create the input for the model
        """
        self.load_column_data()
        self.load_std_scalar()
        self.load_model()

        # Creates an array of shape (1, 8)
        test_array = np.zeros((1, len(self.input_columns['colNames'])))
        
        # Removed burnout_score to match your training data
        test_array[0,0] = self.input_columns['day_type'][str(self.data['day_type']).capitalize()] # Handles string casing if needed
        test_array[0,1] = self.data['work_hours']
        test_array[0,2] = self.data['screen_time_hours']
        test_array[0,3] = self.data['meetings_count']
        test_array[0,4] = self.data['breaks_taken']
        test_array[0,5] = self.data['after_hours_work']
        test_array[0,6] = self.data['sleep_hours']
        test_array[0,7] = self.data['task_completion_rate']

        self.test_df = pd.DataFrame(test_array, columns=self.input_columns['colNames'])
        self.test_df_scaled = self.std_scalar.transform(self.test_df)

        return self.test_df_scaled
    
    def predict_burnout(self, user_input_data):
        """"
        This function is to predict the burnout score
        """
        self.data = dict(user_input_data)
        
        # Ensure day_type is a string to map to the JSON dictionary properly
        self.data['day_type'] = str(self.data.get('day_type', 'Weekday')) 
        
        self.data['work_hours'] = float(self.data['work_hours'])
        self.data['screen_time_hours'] = float(self.data['screen_time_hours'])
        self.data['meetings_count'] = int(self.data['meetings_count'])
        self.data['breaks_taken'] = int(self.data['breaks_taken'])
        self.data['after_hours_work'] = int(self.data['after_hours_work'])
        self.data['sleep_hours'] = float(self.data['sleep_hours'])
        self.data['task_completion_rate'] = float(self.data['task_completion_rate'])
        # Removed burnout_score parsing
        
        self.create_input()
        
        # Extract the scalar value from the returned nested array (e.g., [[45.2]])
        self.prediction = self.model.predict(self.test_df_scaled)
        self.final_prediction = float(np.around(self.prediction[0][0], 2))
        
        return self.final_prediction

    def save_data_in_db(self, input_data):
        """"
        This function is to save the input data in the database
        """
        data_to_save = dict(self.data)
        data_to_save.update({'Prediction': self.final_prediction})
        
        data_collection = get_data_collection()
        data_collection.insert_one(data_to_save)
        return