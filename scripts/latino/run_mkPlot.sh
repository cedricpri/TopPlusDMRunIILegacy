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
    echo ''
    exit
else
    if [ $1 == '-1' ]; then
	YEAR='2016-2017-2018'
    elif [ $1 == '0' ]; then
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
    else 
	TAG=$2
    fi
    if [ $# -lt 3 ]; then
	SIGSET='SM'
    else
	SIGSET=$3
    fi
    if [ $# -lt 4 ]; then
	FILESET=$SIGSET
        NORM='None'
    elif [ $# -eq 4 ]; then
        if [ $4 == 'Norm' ] || [ $4 == 'CRnorm' ] || [ $4 == 'PreFit' ] || [ $4 == 'PostFit' ] || [ $4 == 'PostFitS' ]; then 
	    NORM=$4
	    FILESET=$SIGSET
	else
	    NORM='None'
	    FILESET=$4
	fi
    else
        if [ $4 == 'Norm' ] || [ $4 == 'CRnorm' ] || [ $4 == 'PreFit' ] || [ $4 == 'PostFit' ] || [ $4 == 'PostFitS' ]; then 
	    NORM=$4
	    FILESET=$5
	else
	    NORM=$5
	    FILESET=$4
	fi
    fi
fi

PLOTDIR=./Plots/$YEAR/$TAG
mkdir -p $PLOTDIR

cp ./Plots/index.php ./Plots/$YEAR/
cp ./Plots/index.php $PLOTDIR/

NUISANCES=nuisances.py
if [[ $NORM == *'PreFit'* ]] || [[ $NORM == *'PostFit'* ]]; then
    ./mergeShapesPostFit.py --years=$YEAR --tag=$TAG --masspoint=$SIGSET --postFit=$NORM
elif [[ $YEAR == *'-'* ]]; then
    ./mergeShapes.py --years=$YEAR --tag=$TAG --sigset=$SIGSET --saveNuisances
    NUISANCES=nuisances_${YEAR}_${TAG}_${SIGSET}.py
fi

if [[ $SIGSET == 'SM'* ]] || [[ $SIGSET == 'Backgrounds'* ]]; then
    if [ $NORM == 'Norm' ]; then
	mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=$PLOTDIR --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --plotNormalizedDistributions=1 --nuisancesFile=None --showIntegralLegend=1 --onlyPlot cratio
    elif [ $NORM == 'CRnorm' ]; then
	mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=$PLOTDIR --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --plotNormalizedCRratio=1 --nuisancesFile=$NUISANCES --onlyPlot cratio
    elif [[ $NORM == *'PreFit'* ]] || [[ $NORM == *'PostFit'* ]]; then
        IFS=- read -ra YEARLIST <<< $YEAR
        if [[ $YEAR == *'-'* ]]; then
            YEARLIST+=( $YEAR )
        fi
        for FITYEAR in "${YEARLIST[@]}"; do
            PLOTDIR=./Plots/$YEAR/$NORM$TAG
            CLEANDIR=$PLOTDIR
            mkdir -p $PLOTDIR
            cp ./Plots/index.php $PLOTDIR/
            if [[ $YEAR == *'-'* ]]; then
                PLOTDIR=./Plots/$YEAR/$NORM$TAG/$FITYEAR
                CLEANDIR=./Plots/$YEAR/$NORM$TAG/*/
                mkdir -p $PLOTDIR
                cp ./Plots/index.php $PLOTDIR/
            fi
            mkPlot.py --pycfg=configuration.py --tag=$FITYEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_$NORM${TAG}_$FILESET.root --outputDirPlots=$PLOTDIR --postFit=p --showDataVsBkgOnly --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --showIntegralLegend=1  --nuisancesFile=None --onlyPlot cratio
        done
        PLOTDIR=$CLEANDIR
    else
	mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=$PLOTDIR --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --showIntegralLegend=1  --nuisancesFile=$NUISANCES --fileFormats='png,root,pdf' --onlyPlot cratio
    fi
else 
    mkPlot.py --pycfg=configuration.py --tag=$YEAR$TAG --sigset=$SIGSET --inputFile=./Shapes/$YEAR/$TAG/plots_${TAG}_$FILESET.root --outputDirPlots=$PLOTDIR --maxLogCratio=1000 --minLogCratio=0.1 --scaleToPlot=2 --nuisancesFile=None --showIntegralLegend=1 --fileFormats='png,root,pdf' --onlyPlot cratio
fi 

if [[ $YEAR == *'-'* ]] && [[ $NORM != *'Fit'* ]]; then # To keep clean
    rm nuisances_${YEAR}_${TAG}_${SIGSET}.py
fi

if [ $# -lt 6 ]; then
    
    if [[ $SIGSET == 'SM'* ]]; then  
	rm $PLOTDIR/c_*
	rm $PLOTDIR/log_c_*
    else
	rm $PLOTDIR/cratio_*
	rm $PLOTDIR/log_cratio_*
    fi
    rm $PLOTDIR/cdifference*
    rm $PLOTDIR/log_cdifference*
fi

