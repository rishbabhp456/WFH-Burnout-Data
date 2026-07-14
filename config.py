import os

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8000

MONGO_PASSWORD = 'test123$'
MONGO_URL = f'mongodb+srv://rishabhp:{MONGO_PASSWORD}@docdb-cluster-20260630-0923.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000'
db_name = 'wfh_burnout'
collection_data = 'burnout_data'
collection_user = 'wfh_users'

MODEL_PATH = os.path.join(os.getcwd(), 'artifacts', 'MLP_Trained_Model.keras')
COLUMN_DATA_PATH = os.path.join(os.getcwd(), 'artifacts', 'MLP_col_data.json')
STD_SCALAR_PATH = os.path.join(os.getcwd(), 'artifacts', 'std_scalar.pkl')
