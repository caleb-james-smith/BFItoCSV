# ProcessCSV.py

import pandas as pd
import numpy as np
import pprint
import os

# TODO

# DONE
# - for 0L, do not use gold, silver, bronze (they do not exist); add all bins
# - fix first column
# - skip -999 values
# - run over all background
# - fix signal name
# - test on signal and background

# get yields and errors from data
def getValues(data):
    yields = []
    errors = []
    # get yields and errors
    for entry in data:
        entry_list  = entry.split(" ")
        bin_yield   = float(entry_list[5])
        bin_error   = float(entry_list[6])
        # skip bin_yield = -999:
        if bin_yield == -999.0:
            continue
        yields.append(bin_yield)
        errors.append(bin_error)
    return yields, errors

def Decode(input_dir, input_file):
    background  = []
    signal      = []
    info        = []
    f = open(input_dir + "/" + input_file, "r")
    for x in f:
        #print("x = {0}".format(x))
        
        # add ttbar
        # if "ttbar" in x:
        #     background.append(x.replace("\n",''))
        #     #print("ttbar found in {0}".format(x))
        # add all-bkg
        if "all-bkg" in x:
            background.append(x.replace("\n",''))
            #print("all-bkg found in {0}".format(x))
        #elif "T4bd_5000490" in x:
        elif "T4bd" in x:
            #print("signal found in {0}".format(x))
            signal.append(x.replace("\n",''))
    info.append(input_file)
    info.append(background)
    info.append(signal)
    
    return info

def Sum(input_dir, input_file):
    #print("input_file: {0}, input_dir: {1}".format(input_file, input_dir))
    #print("input_dir: {0}, input_file: {1}".format(input_dir, input_file))
    #print(" --- {0}".format(input_file))

    info        = Decode(input_dir, input_file)
    name        = info[0]
    background  = info[1]
    signal      = info[2]
    master_list = []

    background_yield, background_error  = getValues(background)
    signal_yield, signal_error          = getValues(signal)
    
    background_yield    = np.array(background_yield)
    background_error    = np.array(background_error)
    signal_yield        = np.array(signal_yield)
    signal_error        = np.array(signal_error)
    
    master_list.append(str(name))
    if len(background_yield) > 0:
        master_list.append(str(np.sum(background_yield)))
        master_list.append(str(np.sqrt(np.sum(np.square(background_error)))))
    elif len(background_yield) == 0:
        master_list.append("0")
        master_list.append("0")
    if len(signal_yield) > 0:
        master_list.append(str(np.sum(signal_yield)))
        master_list.append(str(np.sqrt(np.sum(np.square(signal_error)))))
    elif len(signal_yield) == 0:
        master_list.append("0")
        master_list.append("0")
    
    master_string = ",".join(master_list)

    # append to csv files
    if "gold" in master_string.lower():
        f = open(input_dir + "_gold.csv", "a")
        f.write(master_string + "\n")
        f.close()
    elif "slvr" in master_string.lower():
        f = open(input_dir + "_silver.csv", "a")
        f.write(master_string + "\n")
        f.close()
    elif "bron" in master_string.lower():
        f = open(input_dir + "_bronze.csv", "a")
        f.write(master_string + "\n")
        f.close()
    else:
        f = open(input_dir + "_zero.csv", "a")
        f.write(master_string + "\n")
        f.close()


def Finder(input_dir, cat_dir, header):
    full_dir = "{0}/{1}".format(input_dir, cat_dir)
    lepton_types = ["gold", "silver", "bronze", "zero"]
    
    print(" - {0}".format(full_dir))
    
    # write headers to csv files
    for lepton_type in lepton_types:
        f_name = "{0}_{1}.csv".format(full_dir, lepton_type)
        f = open(f_name, "w")
        f.write(header)
        f.flush()

    gold    = []
    silver  = []
    bronze  = []
    zero    = []

    for root, dirs, files in os.walk(full_dir, topdown=False):
        #n_files = len(files)
        #print("In Finder(): root: {0}, dirs: {1}, n_files: {2}".format(root, dirs, n_files))
        for name in files:
            name_lower = os.path.join(name).lower()
            #print("name: {0}, name_lower: {1}".format(name, name_lower))
            
            # skip vim swap files from files open in vim, i.e. ".file.csv.swp"
            if ".swp" in name_lower:
                continue
            
            # lepton types: use analysis names
            if "gold" in name_lower:
                gold.append(os.path.join(name))
            elif "slvr" in name_lower:
                silver.append(os.path.join(name))
            elif  "bron" in name_lower:
                bronze.append(os.path.join(name))
            else:
                zero.append(os.path.join(name))
    
    for x in gold:
        Sum(full_dir, x)
    for x in silver:
        Sum(full_dir, x)
    for x in bronze:
        Sum(full_dir, x)
    for x in zero:
        Sum(full_dir, x)
    
def Summary(input_file):
    df              = pd.read_csv(input_file)
    Background      = df["Background"].to_numpy()
    Background_Err  = df["Background_Err"].to_numpy()
    Signal          = df["Signal"].to_numpy()
    Signal_Err      = df["Signal_Err"].to_numpy()

    sum_background      = str(np.sum(Background))
    sum_signal          = str(np.sum(Signal))
    sum_background_err  = str(np.sqrt(np.sum(np.square(Background_Err))))
    sum_signal_err      = str(np.sqrt(np.sum(np.square(Signal_Err))))
    result              = [sum_background, sum_background_err, sum_signal, sum_signal_err]
    
    return result

def SumFind(input_dir, sample):
    print("Processing input directory: {0}".format(input_dir))
    
    header = "Name,Background,Background_Err,Signal,Signal_Err\n"
    categories = ["0L", "1L", "2L", "3L"]

    for cat in categories:
        cat_dir = "{0}_{1}".format(sample, cat)
        Finder(input_dir, cat_dir, header)

    summary_list = []

    for root, dirs, files in os.walk(input_dir, topdown=False):
        #n_files = len(files)
        #print("In SumFind(): root: {0}, dirs: {1}, n_files: {2}".format(root, dirs, n_files))
        for name in files:
            output = "{0}/{1}".format(root, name)
            if sample in name:
                # remove .csv extension
                name_clean = name.replace(".csv", "")
                #print("name: {0}, name_clean: {1}".format(name, name_clean))
                values  = Summary(output)
                line    = [name_clean] + values
                summary_list.append(line)
    
    #print(summary_list)

    summary_file = "{0}/Summary.csv".format(input_dir)
    f = open(summary_file, "w")
    f.write(header)
    for line in summary_list:
        f.write(",".join(line) + "\n")
    f.close()

def main():
    # --- Sum background --- #
    #input_dir   = "BFI_NanoAODv9_T4bd_allbkg_2022_09_28_v1"
    #sample      = "BG"
    #SumFind(input_dir, sample)
    #input_dir   = "BFI_NanoAODv9_T4bd_ttbar_2022_09_28_v1"
    #sample      = "BG"
    #SumFind(input_dir, sample)
    #input_dir   = "BFI_NanoAODv9_T4bd_ttbar_2022_10_03_v1"
    #sample      = "BG"
    #SumFind(input_dir, sample)
    #input_dir   = "BFI_Alice_NanoAODv9_T4bd_ttbar_2022_10_03_v1"
    #sample      = "BG"
    #SumFind(input_dir, sample)
    #input_dir   = "BFI_Alice_NanoAODv9_T4bd_ttbar_2022_10_03_v2"
    #sample      = "BG"
    #SumFind(input_dir, sample)
    input_dir   = "BFI_NanoAODv9_T4bd_allbkg_2022_10_03_v2"
    sample      = "BG"
    SumFind(input_dir, sample)
    input_dir   = "BFI_NanoAODv9_T4bd_ttbar_2022_10_03_v2"
    sample      = "BG"
    SumFind(input_dir, sample)
    
    # --- Sum signal --- #
    #input_dir   = "BFI_NanoAODv9_T4bd_allbkg_2022_09_28_v1_Signal"
    #sample      = "T4bd"
    #SumFind(input_dir, sample)
    #input_dir   = "BFI_NanoAODv9_T4bd_ttbar_2022_09_28_v1_Signal"
    #sample      = "T4bd"
    #SumFind(input_dir, sample)
    input_dir   = "BFI_NanoAODv9_T4bd_allbkg_2022_10_03_v2_Signal"
    sample      = "T4bd"
    SumFind(input_dir, sample)
    input_dir   = "BFI_NanoAODv9_T4bd_ttbar_2022_10_03_v2_Signal"
    sample      = "T4bd"
    SumFind(input_dir, sample)

if __name__ == '__main__':
    main()

