#!/bin/bash
# PATHOF SCRIPT: /BIOMAG_DATA/scripts/
# example:  bash /BIOMAG_DATA/scripts/pm_extract_dicomzip.sh . 20*_dicom.zip T1_RAW 192 RS_RAW 250 STIM_RAW 1500
#           help: bash /BIOMAG_DATA/scripts/pm_extract_dicomzip.sh
# SUPERBATCH: pm_subfolder pwd bash /BIOMAG_DATA/scripts/pm_extract_dicomzip.sh . 20*_dicom.zip T1_RAW 192 RS_RAW 250 STIM_RAW 1500
#                   this will extract all subdirectories in a root DIR

if [ "$#" -lt 4 ]; then
	echo "Usage: pm_extract_dicomzip.sh SUBJECT_FOLDER ZIP_SEARCHSTRING [arguments]"
	echo "  SUBJECT_FOLDER: enthält die RAW-DATEN eines Subjects"
	echo "	ZIP_SEARCHSTRING: z.b. 2020*_dicom.zip"
    echo "  ie: bash pm_extract_dicomzip.sh . 20*_dicom.zip T1_RAW 192 RS_RAW 250 STIM_RAW 1500"
	exit 1
fi

start=`date +%s`

## PARSE THE ARGUMENTS AND STORE THEM IN AN ASSOCIATIVE ARRAY
        declare -A SIZE
        FIELDNAME=''
        PROJECT_STR=''
        FILE_STR=''
        # PARSE THROUGH ARGUMENTS: arg1: PROJECT_NAME, arg2: ZIP_FILE_STR, arg3: SEQ_TYPE, arg4: NUMOFIMAGES
        CC=0;
        ARGLIST=''
        for arg in "$@"; do
            CC=$((CC+1))
            if [ $CC -eq 1 ]; then
                SUBJ=$arg;
                if [ $SUBJ == "pwd" ]; then
                    SUBJ=$(pwd)
                fi
                if [ $SUBJ == "." ]; then
                    SUBJ=$(pwd)
                fi
            elif [ $CC -eq 2 ]; then
                FILE_STR=$arg;
            else
                REST=$[$CC%2==0];
                if [ $REST -eq 0 ]; then
                    #GERADE
                    # echo $CC ': gerade'
                    FIELDNAME=$arg
                    ARGLIST="$ARGLIST $arg: "
                else
                    #UNGERADE
                    # echo $CC ' : ungerade'
                    SIZE[$FIELDNAME]=$arg
                    ARGLIST="$ARGLIST $arg"
                fi
            fi
        done

echo "Parse parameters:"
echo "+ Subject_dir: " $SUBJ
echo "+ File: " $FILE_STR
echo "+ ARG: " $ARGLIST


# # EXTRACT A ZIP FILE IF FOUND IN THE FOLDER
## EXTRACT THE ZIPFILE
ZIPFILE="$SUBJ/$FILE_STR"
ZIPPED=false
if [ -f  $ZIPFILE ]; then
    echo $ZIPFILE
    mkdir -p $SUBJ/TMP
    unzip -o $ZIPFILE -d $SUBJ/TMP/
    ZIPPED=true
else
    ls $ZIPFILE
    exit
fi

## NOW LOOP THROUGH SUBDIRS IN THEM TEMP_ZIP UND COMPARE FILE_COUNT WITH THE SIZE_ARRAY
for pn in $(find $SUBJ/TMP/ -mindepth 2 -maxdepth 4 -type d | sort)
do
    echo "$pn"

    ff="$(ls -A $pn | wc -l)"
    echo "+ files: $ff"

    # # ACCESS the ASSOCIATIVE ARRAY SIZE by KEY
    for key in "${!SIZE[@]}"
    do
        # echo "$key = ${SIZE[$key]}"
        if [ $ff -eq ${SIZE[$key]} ]; then
            echo "+ identified as: $key "
            TARG_DIR_IND=1
            TARG_DIR="$SUBJ/$key"
            while [ -d $TARG_DIR"_"$TARG_DIR_IND ]
            do
                TARG_DIR_IND=$((TARG_DIR_IND+1))
            done
            cmd="mv $pn ${TARG_DIR}_${TARG_DIR_IND}"
            echo $cmd
            $cmd
            echo
            break
        fi
    done
done

## remove the ZIPFOLDER
if [ $ZIPPED ]; then
    rm -rf $SUBJ/TMP
fi

## finish
echo "Fertig :-)"
