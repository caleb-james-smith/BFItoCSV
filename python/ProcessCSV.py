# ProcessCSV.py

import pandas as pd
import numpy as np
import pprint
import os


# TODO
# - do not add negative values (e.g. -999)
# - for 0L, do not use gold, silver, bronze (they do not exist); add all bins
# - test on signal and background

def Decode(input_name, b):
    background  = []
    signal      = []
    Info        = []
    f = open(b+"/"+input_name, "r")
    for x in f:
        if "ttbar" in x:
            background.append(x.replace("\n",''))
        elif "signal" in x:
            signal.append(x.replace("\n",''))
    Info.append(input_name)
    Info.append(background)
    Info.append(signal)
    
    return Info

def Sum(input_name, b):
    a           = Decode(input_name,b)
    name        = a[0]
    background  = a[1]
    signal      = a[2]
    l           = []
    
    #print(name)

    ts  = []
    te  = []
    cps = []
    cpe = []

    for i in background:
        d = i.split(" ")
        ts.append(float(d[5]))
        te.append(float(d[6]))

    for j in signal:
        k = j.split(" ")
        cps.append(float(k[5]))
        cpe.append(float(k[6]))
    
    e = np.array(ts)
    r = np.array(te)
    y = np.array(cps)
    u = np.array(cpe)
    
    l.append(str(name))
    if len(e)>0:
        l.append(str(np.sum(e)))
        l.append(str(np.sqrt(np.sum(np.square(r)))))
    elif len(e)==0:
        l.append("0")
        l.append("0")
    if len(y)>0:
        l.append(str(np.sum(y)))
        l.append(str(np.sqrt(np.sum(np.square(u)))))
    elif len(y)==0:
        l.append("0")
        l.append("0")
    h = ",".join(l)

    # append to csv files
    if "gold" in h.lower():
        file1 = open(b+"_gold.csv", "a")
        file1.write(h+"\n")
        file1.close()
    elif "slvr" in h.lower():
        file2 = open(b+"_silver.csv", "a")
        file2.write(h+"\n")
        file2.close()
    elif "bron" in h.lower():
        file3 = open(b+"_bronze.csv", "a")
        file3.write(h+"\n")
        file3.close()
    else:
        file1 = open(b+"_zero.csv", "a")
        file1.write(h+"\n")
        file1.close()

    return h


def Finder(input_dir, b):
    cat_dir = "{0}/{1}".format(input_dir, b)
    header = "Name,TTbar,TTbar_Err,Signal,Signal_Err\n"
    
    # write headers
    file1 = open(cat_dir + "_gold.csv", "w")
    file1.write(header)
    file1.flush()

    file2 = open(cat_dir + "_silver.csv", "w")
    file2.write(header)
    file2.flush()

    file3 = open(cat_dir + "_bronze.csv", "w")
    file3.write(header)
    file3.flush()
    
    file1 = open(cat_dir + "_zero.csv", "w")
    file1.write(header)
    file1.flush()

    gold    = []
    silver  = []
    bronze  = []
    zero    = []

    for root, dirs, files in os.walk(cat_dir, topdown=False):
    #for root, dirs, files in os.walk("./"+b, topdown=False):
        n_files = len(files)
        print("In Finder(): root: {0}, dirs: {1}, n_files: {2}".format(root, dirs, n_files))
        for name in files:
            if "gold" in os.path.join(name).lower():
                gold.append(os.path.join(name))
            elif "slvr" in os.path.join(name).lower():
                silver.append(os.path.join(name))
            elif  "bron" in os.path.join(name).lower():
                bronze.append(os.path.join(name))
            else:
                zero.append(os.path.join(name))
    
    for x in gold:
        Sum(x, cat_dir)
    for x in silver:
        Sum(x, cat_dir)
    for x in bronze:
        Sum(x, cat_dir)
    for x in zero:
        Sum(x, cat_dir)
    
def Summary(i):
    df = pd.read_csv(i)
    TTbar = df["TTbar"].to_numpy()
    TTbar_Err = df["TTbar_Err"].to_numpy()
    Signal = df["Signal"].to_numpy()
    Signal_Err = df["Signal_Err"].to_numpy()

    tt      = str(np.sum(TTbar))
    cp      = str(np.sum(Signal))
    terr    = str(np.sqrt(np.sum(np.square(TTbar_Err))))
    cperr   = str(np.sqrt(np.sum(np.square(Signal_Err))))
    u       = [tt,terr,cp,cperr]
    return u

def SumFind(input_dir, sample):
    Finder(input_dir, sample+"_0L")
    Finder(input_dir, sample+"_1L")
    Finder(input_dir, sample+"_2L")
    Finder(input_dir, sample+"_3L")
    
    l = []
    for root, dirs, files in os.walk(input_dir, topdown=False):
    #for root, dirs, files in os.walk("./", topdown=False):
        n_files = len(files)
        print("In SumFind(): root: {0}, dirs: {1}, n_files: {2}".format(root, dirs, n_files))
        #print("root: {0}, dirs: {1}, files: {2}".format(root, dirs, files))
        for name in files:
            output = "{0}/{1}".format(root, name)
            #print("In SumFind(): output: {0}".format(output))
            if sample in name:
                l.append(name)
                l.append(",".join(Summary(output)))
                l.append("\n")
    
    #print(",".join(l))

    summary_file = "{0}/Summary.csv".format(input_dir)
    f = open(summary_file, "w")
    f.write(",".join(l))
    f.close()

def main():
    input_dir   = "BFI_NanoAODv9_T4bd_allbkg_2022_09_28_v1"
    sample      = "BG"
    SumFind(input_dir, sample)
    input_dir   = "BFI_NanoAODv9_T4bd_ttbar_2022_09_28_v1"
    sample      = "BG"
    SumFind(input_dir, sample)

if __name__ == '__main__':
    main()

