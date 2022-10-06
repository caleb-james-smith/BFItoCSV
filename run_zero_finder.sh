#!/usr/bin/bash

#ARG is directory where your csv files are
#output prints to screen so pipe into a text file

#CSVDIR=BFI_NanoAODv9_T4bd_allbkg_2022_09_28_v1
#python3 zero_finder.py ${CSVDIR} > zeros_${CSVDIR}.log
#
#CSVDIR=BFI_NanoAODv9_T4bd_ttbar_2022_09_28_v1
#python3 zero_finder.py ${CSVDIR} > zeros_${CSVDIR}.log

CSVDIR=BFI_NanoAODv9_T4bd_allbkg_2022_10_03_v2
python3 zero_finder.py ${CSVDIR} > zeros_${CSVDIR}.log

CSVDIR=BFI_NanoAODv9_T4bd_ttbar_2022_10_03_v2
python3 zero_finder.py ${CSVDIR} > zeros_${CSVDIR}.log


