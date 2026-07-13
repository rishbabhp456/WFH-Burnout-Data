import os,json,numpy as np

json_path = os.path.join(os.getcwd(), 'artifacts', 'MLP_col_data.json')

with open(json_path,'r') as f:
    input_columns = json.load(f)
    print(json_path,"")

def test():
    test_array = np.zeros((1,len(input_columns['colNames'])))
    print(test_array)
    return test_array

test_array = test()