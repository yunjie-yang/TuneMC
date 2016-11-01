import json
import os
def generate_pars_dict():
    WorkHOME = os.environ['WorkHOME']
    pars_info = {'alphaSvalue':{'min':0.06,'max':0.25,'Monash':0.1365,'block':1,'category':'TimeShower'},
                 'pTmin':{'min':0.1,'max':2.0,'Monash':0.5,'block':1,'category':'TimeShower'},
                 'pTminChgQ':{'min':0.1,'max':2.0,'Monash':0.5,'block':1,'category':'TimeShower'},
                 'sigma':{'min':0.0,'max':1.0,'Monash':0.335,'block':2,'category':'StringPT'},
                 'bLund':{'min':0.2,'max':2.0,'Monash':0.98,'block':2,'category':'StringZ'},
                 'aExtraSQuark':{'min':0.0,'max':2.0,'Monash':0.0,'block':2,'category':'StringZ'},
                 'aExtraDiquark':{'min':0.0,'max':2.0,'Monash':0.97,'block':2,'category':'StringZ'},
                 'rFactC':{'min':0.0,'max':2.0,'Monash':1.32,'block':2,'category':'StringZ'},
                 'rFactB':{'min':0.0,'max':2.0,'Monash':0.855,'block':2,'category':'StringZ'},
                 'probStoUD':{'min':0.0,'max':1.0,'Monash':0.217,'block':3,'category':'StringFlav'},
                 'probQQtoQ':{'min':0.0,'max':1.0,'Monash':0.081,'block':3,'category':'StringFlav'},
                 'probSQtoQQ':{'min':0.0,'max':1.0,'Monash':0.915,'block':3,'category':'StringFlav'},
                 'probQQ1toQQ0':{'min':0.0,'max':1.0,'Monash':0.0275,'block':3,'category':'StringFlav'},
                 'etaSup':{'min':0.0,'max':1.0,'Monash':0.6,'block':3,'category':'StringFlav'},
                 'etaPrimeSup':{'min':0.0,'max':1.0,'Monash':1.0,'block':3,'category':'StringFlav'},
                 'decupletSup':{'min':0.0,'max':1.0,'Monash':1.0,'block':3,'category':'StringFlav'},
                 'mesonUDvector':{'min':0.0,'max':3.0,'Monash':0.5,'block':3,'category':'StringFlav'},
                 'mesonSvector':{'min':0.0,'max':3.0,'Monash':0.55,'block':3,'category':'StringFlav'},
                 'mesonCvector':{'min':0.0,'max':3.0,'Monash':0.88,'block':3,'category':'StringFlav'},
                 'mesonBvector':{'min':0.0,'max':3.0,'Monash':2.2,'block':3,'category':'StringFlav'}
                }
    with open('{}/utils/all_pars_dict.json'.format(WorkHOME),'w') as all_pars_dict:
        json.dump(pars_info,all_pars_dict,sort_keys=True, indent=4)


def load_config(config_file):
    try:
        with open(config_file,'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except:
        raise Exception('json file loading failed. Please check commas or parentheses?')
        
def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError("Cannot covert string {} to a bool.".format(s))

def params_to_tune(blocks):
    
    WorkHOME = os.environ['WorkHOME']
   
    pars_info = load_config('{}/utils/all_pars_dict.json'.format(WorkHOME))
 
    param_list = open('{}/pythia_space/pars_to_tune.txt'.format(WorkHOME),'w')
    
    for index,block in enumerate(blocks):
        if block:
            block_number = index+1
            for par in pars_info:
                if int(pars_info[par]['block'])==block_number:
                    param_list.write('{}\n'.format(par))
    
    param_list.close()
