#!/bin/bash

if [ $# == 0 ]; then
    echo ''
    echo 'Please provide data taking year:'; 
    echo '  0. 2016 '
    echo '  1. 2017'
    echo '  2. 2018'
    echo ''
    exit
elif [ $# == 1 ]; then
    echo ''
    echo 'Please provide tag value:'; 
    echo '  0. Preselection: shapes for data/MC comparison of various kinematic observables '
    echo '  1. ValidationRegions'
    echo '  2. StopSignalRegions'
    echo ''
    exit
else
    if [ $1 == '0' ]; then
	YEAR='2016'
    elif [ $1 == '1' ]; then
	YEAR='2017'
    elif [ $1 == '2' ]; then
	YEAR='2018'	
    else 
	YEAR=$1
    fi
    if [ $2 == '0' ]; then
	TAG='Preselection'
    elif [ $2 == '1' ]; then
	TAG='ValidationRegions'
    elif [ $2 == '2' ]; then
	TAG='StopSignalRegions'
    else 
	TAG=$2
    fi
    if [ $# == 2 ] || [ $3 == '0' ] || [ $3 == 'shapes' ]; then
	BATCH=True
	if [[ "$HOSTNAME" = *"ifca"* ]]; then
	    QUEUE=gridui_sort
	else
	    QUEUE=testmatch
	fi
	DOHADD=False
	KEEPINPUT=False
    else
	BATCH=False
	QUEUE=''
	DOHADD=True
	KEEPINPUT=True
    fi
    if [ $# -lt 4 ]; then
	SIGSET='SM'
	if [ $TAG == 'btagefficiencies' ]; then
	    SIGSET='Backgrounds'
	fi
	SPLIT='Samples'
    else
	SIGSET=$4
	if [ $# -lt 5 ]; then
	    SPLIT='Samples'
	else
	    if [ $5 == 'tomorrow' ] || [ $5 == 'workday' ] || [ $5 == 'gridui_medium' ] ; then
		QUEUE=$5
		if [ $# -lt 6 ]; then
		    SPLIT='Samples'
		else
		    SPLIT=$6
		fi
	    else
		SPLIT=$5
	    fi
	fi
    fi
fi

mkdir -p ./Shapes/$YEAR/$TAG/$SPLIT

if [ $BATCH == True ]; then
    mkShapes.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --treeName=Events --outputDir=./Shapes/$YEAR/$TAG/$SPLIT --doBatch=True --batchQueue=$QUEUE --batchSplit=$SPLIT
else 
    rm -f ./Shapes/$YEAR/$TAG/$SPLIT/*_temp*.root
    mkShapes.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --treeName=Events --outputDir=./Shapes/$YEAR/$TAG/$SPLIT --batchSplit=$SPLIT --doHadd=True --doNotCleanup
    if [[ "$SIGSET" == "Backgrounds"* && "$SIGSET" != "Backgrounds-"*  && "$SIGSET" != "Backgrounds" ]] || [[ "$SIGSET" == "Data" ]]; then
	ONLYSAMPLE=${SIGSET#Backgrounds}
	if [ "$ONLYSAMPLE" == "Data" ]; then
	    ONLYSAMPLE="DATA"
	fi
	mv ./Shapes/$YEAR/$TAG/$SPLIT/plots_$YEAR$TAG.root ./Shapes/$YEAR/$TAG/Samples/plots_$YEAR${TAG}_ALL_${ONLYSAMPLE}.root
    else
	mv ./Shapes/$YEAR/$TAG/$SPLIT/plots_$YEAR$TAG.root ./Shapes/$YEAR/$TAG/plots_${TAG}_${SIGSET}.root 
    fi
    rm -f ./Shapes/$YEAR/$TAG/$SPLIT/*_temp*.root
fi

#mkShapes.py --pycfg=configuration.py --tag=$TAG --treeName=Events --outputDir=./Shapes --doBatch=$BATCH --batchQueue=$QUEUE --batchSplit=Samples --doHadd=$DOHADD --doNotCleanup]==$KEEPINPUT
