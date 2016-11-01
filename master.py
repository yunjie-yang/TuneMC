import os
import json
from utils.general_utils import load_config
from utils.spearmint_utils import start_spearmint_tune

def main():
    config = load_config('tune_config.json') 
    WorkHOME = config['WorkHOME']
    spearmint_dir = config['spearmint_dir']
    
    os.environ['WorkHOME'] = WorkHOME

    print WorkHOME

    start_spearmint_tune(spearmint_dir,WorkHOME,True)

if __name__ == '__main__':
    main()
