# Script, um Rekursiv bestimmte Unterordner zu verschieben. Sinnvolles Szenario ist hier z.B. das verschieben von vorverarbeiteten Daten aus einem /raw/subj1 nach /processed_final/subj1
## start via: 
#* /bin/bash /BIOMAG_DATA/scripts/pm_move_subfolders.sh

# BEISPIEL
# /bin/bash /BIOMAG_DATA/scripts/pm_move_subfolders.sh /BIOMAG_DATA/Projects/REHA_CONN_CD/data/raw/MRT_Rehaconn_3T_complete/I2_MRT_Verlaufskontrollen /BIOMAG_DATA/Projects/REHA_CONN_CD/data/processed_final "smooth filtered"


if [ "$#" -lt 3 ]; then
	echo "Usage: pm_move_subfolders MAINFOLDER TARGETFOLDER ARG"
	echo '		ie: /bin/bash /BIOMAG_DATA/scripts/pm_move_subfolders.sh /BIOMAG_DATA/Projects/REHA_CONN_CD/data/raw/MRT_Rehaconn_3T_complete/I2_MRT_Verlaufskontrollen /BIOMAG_DATA/Projects/REHA_CONN_CD/data/processed_final "smooth filtered"'
	exit 1
fi

# ARGUMENTS


# #COMPLETE BACKUPS ARE DONE FOR: /STORAGE, /LIB, /scripts
RSYNC=();

for d in $(find $1 -maxdepth 1 -type d ! -path $1)
do
  	#get the subject_name of this folder
	subjname="$(basename $d)"
	
	for subdir in $3; do
		# echo "Suche nach: $subdir in $subjname"
		tmp_dir="$d/$subdir*"
		for dir2move in $(find $tmp_dir -maxdepth 1 -type d); do
			dir_found="$(basename $dir2move)"
			dir_target="$2/$subjname/"
			RSYNC+=("mv $dir2move $dir_target")
		done
	done
		
done

## print the RSYNC command
echo "Gefundene Ordner:"
for i in "${!RSYNC[@]}"; 
do
	cmd="${RSYNC[$i]}"
	echo "$(($i+1))/${#RSYNC[@]}: $cmd"; 
	# $cmd
done

echo "Wirklich ausführen?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) 
			echo 'Beginne Löschung'
			for i in "${!RSYNC[@]}"; 
			do
				cmd="${RSYNC[$i]}"
				echo "$(($i+1))/${#RSYNC[@]}: $cmd"; 
				$cmd
			done

			echo "fertig :-)"
			break;;
        No ) 
			exit;;
    esac
done

