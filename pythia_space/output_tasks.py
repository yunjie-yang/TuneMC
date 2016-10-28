import numpy as np
import csv
from math import sqrt

def Get_Ratio_Error_Numbers(num,denom):
    num=float(num)
    denom=float(denom)
    value = num/denom
    error = 0.
    if num == 0 and denom != 0:
        error = value * sqrt(1./denom)
    else:
        error = value * sqrt(1./num + 1./denom)
    return error

def check_one_percent(error,value):

    if value != 0.:
        if error/value <= 0.01:
	    return value*0.01
	else:
            return error
    else:
	return error

def compute_chi2(o_value,o_error,t_value,t_error):
    error2 = o_error**2 + t_error**2
    if error2 != 0.:
        return (o_value-t_value)**2/error2
    else:
        return 0.

def combine_output(n_cores,csv_Dir,bin_widths,outputFile_bin_contents,outputFile_bin_errors):
    input_files = []
    for i_job in range(n_cores):
        input_files.append('{}/out_bin_content_{}.csv'.format(csv_Dir,i_job))
        
    combined_bin_content = []
    
    for index,iFile in enumerate(input_files):
        with open(iFile, 'rb') as f:
            reader = csv.reader(f)
            data_list = []
            for row in reader:
                data_list.append([int(i) for i in row])
            data_array = np.array(data_list)
        if index == 0:
            combined_bin_content = data_array.copy()
        else:
            for irow, row in enumerate(combined_bin_content):
                combined_bin_content[irow] = np.add(row,data_array[irow])
    
    output_bin_contents = []
    output_bin_errors   = []
    
    for ihist, hist in enumerate(combined_bin_content):
        content_row = []
        error_row = []
        row_sum = 0
        
        for ibin in range(1,len(hist)-1):
            row_sum += bin_widths[ihist]*hist[ibin]
        
        for ibin in range(1,len(hist)-1):
            content = hist[ibin]/row_sum
            content_row.append(content)
            error = Get_Ratio_Error_Numbers(hist[ibin],row_sum)
            error_row.append(error)
            
        output_bin_contents.append(content_row)            
        output_bin_errors.append(error_row)
    
    content_file = open(outputFile_bin_contents,'w')
    content_file_writer = csv.writer(content_file,delimiter =',',
                                     quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    error_file = open(outputFile_bin_errors,'w')
    error_file_writer = csv.writer(error_file,delimiter =',',
                                   quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)
    
    for ihist in range(len(output_bin_contents)):
        content_file_writer.writerow(output_bin_contents[ihist])
        error_file_writer.writerow(output_bin_errors[ihist])
    
    content_file.close()
    error_file.close()
    
def get_chi2(object_contents,object_errors,tune_contents,tune_errors,output_file):
    
    input_files = [object_contents,object_errors,tune_contents,tune_errors]
    
    lists = []
    
    for index,iFile in enumerate(input_files):
        with open(iFile, 'rb') as f:
            reader = csv.reader(f)
            data_list = []
            for row in reader:
                data_list.append([float(i) for i in row])
            lists.append(np.array(data_list))
    
    sum_chi2 = 0
    chi2s    = []

    ofile = open(output_file,'a')
    ofile_writer = csv.writer(ofile,delimiter =',',
                              quotechar=" ",lineterminator="\n",quoting=csv.QUOTE_ALL)

    for ihist in range(len(lists[0])):
        
        ihist_chi2 = 0
        
        for ibin in range(len(lists[0][ihist])):
            o_value = lists[0][ihist][ibin]
            o_error = lists[1][ihist][ibin]
            t_value = lists[2][ihist][ibin]
            t_error = lists[3][ihist][ibin]
            
            o_error = check_one_percent(o_error,o_value)
            t_error = check_one_percent(t_error,t_value)
            
            chi2 = compute_chi2(o_value,o_error,t_value,t_error)
            
            ihist_chi2 += chi2

        chi2s.append(ihist_chi2)
        sum_chi2 += ihist_chi2
    
    ofile_writer.writerow(chi2s)
    ofile.close()
    
    return sum_chi2
