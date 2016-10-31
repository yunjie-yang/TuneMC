import shutil
import os

from utils.utils import read_setup

setup = read_setup('tune_config.json')

WorkHOME = setup['WorkHOME']

CopyInput = True

Date_Key = '1026'
Call_Key = 'tune_188_1M'

TextsDir = '{}/Spearmint-interface'.format(TuneHOME)
PlotsDir = '{}/Spearmint-space/Plots'.format(TuneHOME)
AnaDir   = '{}/Analysis'.format(TuneHOME)

ResultsDir = '{}/Results/{}_{}'.format(TuneHOME,Date_Key,Call_Key)

if not os.path.exists(ResultsDir):
	os.makedirs(ResultsDir)

PlotNames = ['Time','FoM_evolv','IndChi2_evolv','param_evolv',
	     'Best_params_all','Best_params_RelDiff',
	     'Spearmint_chi2_1D_lin','Spearmint_chi2_1D_log']

InputTextNames = ['results','TimeStamps','IndChi2Evolv']
OutputTextNames = ['Best','best_model_param']

ROOTNames = ['analysis_output_best_observed','analysis_output_best_model','finalOutput_observed','finalOutput_model']

DistNames = ['event_shapes_1_model','event_shapes_2_model','event_shapes_1_observed','event_shapes_2_observed',
	     'string-breaking_kinematics_model','string-breaking_kinematics_observed',
	     'string-breaking_flavor_model','string-breaking_flavor_observed']

RangeTextNames = ['param_ranges_plug_in_03','param_ranges_plug_in_01']

ROOTTextNames = ['FoMs_model','FoMs_observed','params_model','params_observed']

if CopyInput:
    SourceFile = '{}/Spearmint-space/Outputs/Spearmint_output.txt'.format(TuneHOME)
    ObjectFile = '{}/Spearmint_output_{}_{}.txt'.format(ResultsDir,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)

    for InputTextName in InputTextNames:
	SourceFile = '{}/{}.csv'.format(TextsDir,InputTextName)
	ObjectFile = '{}/{}_{}_{}.csv'.format(ResultsDir,InputTextName,Date_Key,Call_Key)
	shutil.copy(SourceFile,ObjectFile)

for PlotName in PlotNames:
    SourceFile = '{}/{}.pdf'.format(PlotsDir,PlotName)
    ObjectFile = '{}/{}_{}_{}.pdf'.format(ResultsDir,PlotName,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)

for OutputTextName in OutputTextNames:
    SourceFile = '{}/{}.csv'.format(TextsDir,OutputTextName)
    ObjectFile = '{}/{}_{}_{}.csv'.format(ResultsDir,OutputTextName,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)

for ROOTName in ROOTNames:
    SourceFile = '{}/{}.root'.format(AnaDir,ROOTName)
    ObjectFile = '{}/{}_{}_{}.root'.format(ResultsDir,ROOTName,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)

for DistName in DistNames:
    SourceFile = '{}/Plots/{}.pdf'.format(AnaDir,DistName)
    ObjectFile = '{}/{}_{}_{}.pdf'.format(ResultsDir,DistName,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)

for RangeTextName in RangeTextNames:
    SourceFile = '{}/Spearmint-space/{}.csv'.format(TuneHOME,RangeTextName)
    ObjectFile = '{}/{}_{}_{}.csv'.format(ResultsDir,RangeTextName,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)

for ROOTTextName in ROOTTextNames:
    SourceFile = '{}/Spearmint-space/ROOT_plotting/{}.csv'.format(TuneHOME,ROOTTextName)
    ObjectFile = '{}/{}_{}_{}.csv'.format(ResultsDir,ROOTTextName,Date_Key,Call_Key)
    shutil.copy(SourceFile,ObjectFile)
