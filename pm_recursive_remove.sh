# Script, um Rekursiv bestimmte Dateien und Ordner zu löschen
## start via: /bin/bash /BIOMAG_DATA/scripts/pm_recursive_remove.sh

# # zum löschen von allen af*.nii files im aktuellen Verzeichnis
# /bin/bash /BIOMAG_DATA/scripts/pm_recursive_remove.sh . af*.nii

# # zum löschen von allen RAW Unterordnern im aktuellen Verzeichnis
# /bin/bash /BIOMAG_DATA/scripts/pm_recursive_remove.sh . RAW/

if [ "$#" -lt 2 ]; then
	echo "Usage: pm_recursive_remove MAINFOLDER CMD ARG"
	echo "		ie: pm_recursive_remove . af*.nii"
	exit 1
fi



# #COMPLETE BACKUPS ARE DONE FOR: /STORAGE, /LIB, /scripts
RSYNC=();

for d in $(find $1 -maxdepth 4 -type d)
do
  	#does the directory exist?
	if test -d "$d/$2"; then
    	echo "$d/$2 exists."
		RSYNC+=("rm -rf $d/$2")
	fi

	if [[ -n $(find $d/ -name "$2" -type f) ]]
	then
		RSYNC+=("rm -rf $d/$2")
	fi
	
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

