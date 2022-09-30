# Overview
The code consists of two stages.
1. C based tool that generates CSV files of yields from BFI <br/>
2. python pandas script that operates on dataframe created from CSV files <br/>

## Instructions on running zero finding tools
1. Make CSV files
    - update run_runBG.sh and put in your root files and output directory
    - do ./run_runBG.sh
	
2. Analyze CSV files (you will need pandas)
    - update run_zero_finder.sh, put in csv directory from the last step and output text file name
    - do ./run_zero_Finder.sh  

## CSV creation
There are two scripts, macroBG.C and macroS.C.
Both take as input the number of leptons and create a directory
which has a csv file for every sub region for the defined lepton multiplicity.
Each csv file contains the yields and errors for every mperp and risr bin.
The signal csv files (macroS) contain all of the mass grid of the specified process.
The BG csv files (macroBG) contain the contributions from all background.

The BFI input files have both "signal like" contributions and fakes (muf0 elf0 ... etc.).
The macro automatically adds the TH1Ds for both signal-like and fakes.

The inputs files that are automatically read in are the BFI root files.
- BG input file is hardcoded on line 268
- Sig input files are passed in on call (they need to follow a naming convention)

## Bash scripts
- runBG.sh: run background over all lepton channels
- runS.sh: run a specific signal over all lepton channels
- run_runBG.sh: run over all backgrounds
- run_runS.sh: run over all signals

## Pandas scripts
These scripts pull together BG and a chosen signal and stitch together all lepton channels
into a single dataframe for analysis.
Much of the content of the scripts are many small analyses that may be commented in and out.
To extract reasonable outputs, there are two approaches.
For each approach, first, pipe the python std out to a file.
```
python script.py > output.x
```
1. printing dataframe.to_csv(index=False) -- this method reanalyzes sliced down frames
2. printing dataframe -- this method is very readable

## Calculate Totals
This script calculates total yields and errors from a set of csv files.
```
python3 python/ProcessCSV.py
```

## Notes

### The "old" directory
The main directory hosts code that operates on the latest version of BFI.
The old directory can be used on the old version with the old naming convention,
specifically "Ch1L-" (old) versus "CH1L_" (new).

### The "old2" directory
This holds versions that operate on BFI versions that are after "old" but before the 2L & 3L flavor consoldation.

