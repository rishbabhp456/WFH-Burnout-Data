import os

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8000

MONGO_URL = 'mongodb://localhost:27017/'
db_name = 'wfh_burnout'
collection_data = 'burnout_data'
collection_user = 'wfh_users'

MODEL_PATH = os.path.join(os.getcwd(), 'artifacts', 'MLP_Trained_Model.keras')
COLUMN_DATA_PATH = os.path.join(os.getcwd(), 'artifacts', 'MLP_col_data.json')
STD_SCALAR_PATH = os.path.join(os.getcwd(), 'artifacts', 'std_scalar.pkl')
