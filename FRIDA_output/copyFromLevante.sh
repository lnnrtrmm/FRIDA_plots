#!/bin/bash


path='/work/mh0033/m300732/FRIDA/FRIDA_uncertaintyOrig/workOutput/'
extension='/detectedParmSpace/PerVarFiles-RDS/'

for expID in 'EMB_26May_nS10000'; do
	mkdir ${expID}

	for filename in $(cat VarList.txt); do
		scp m300732@levante.dkrz.de:${path}${expID}${extension}${filename} $expID/
	done
done
