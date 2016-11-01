import json

def load_config(config_file):
    try:
        with open(config_file,'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except:
        raise Exception('setup.json loading failed. Please check commas or parentheses?')
        
def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError("Cannot covert string {} to a bool.".format(s))
