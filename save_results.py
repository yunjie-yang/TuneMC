import shutil
import os
from utils.utils import load_config

setup = load_config('tune_config.json')

WorkHOME = setup['WorkHOME']

File_Key = '1028_block1_70'

TextsDir = '{}/interface'.format(WorkHOME)
PlotsDir = '{}/spearmint_space/Plots'.format(WorkHOME)

ResultsDir = '{}/results/{}'.format(WorkHOME,File_Key)

if not os.path.exists(ResultsDir):
	os.makedirs(ResultsDir)

PlotNames = ['Time','obj_evolv','ind_chi2_evolv','param_evolv',
	     'Best_params_all','Best_params_RelDiff']
#'Spearmint_chi2_1D_lin','Spearmint_chi2_1D_log']

csvNames = ['results','time_stamps','objectives']
txtNames = ['spearmint_output']

for csvName in csvNames:
    SourceFile = '{}/{}.csv'.format(TextsDir,csvName)
    ObjectFile = '{}/{}_{}.csv'.format(ResultsDir,csvName,File_Key)
    shutil.copy(SourceFile,ObjectFile)

for txtName in txtNames:
    SourceFile = '{}/{}.txt'.format(TextsDir,txtName)
    ObjectFile = '{}/{}_{}.txt'.format(ResultsDir,txtName,File_Key)
    shutil.copy(SourceFile,ObjectFile)

for PlotName in PlotNames:
    SourceFile = '{}/{}.pdf'.format(PlotsDir,PlotName)
    ObjectFile = '{}/{}_{}.pdf'.format(ResultsDir,PlotName,File_Key)
    shutil.copy(SourceFile,ObjectFile)
