# MAIN BACKUPSCRIPT FOR THE BIOMAG DB
## start via: /bin/bash backup_BIOMAG_DATA.sh

# #FOLDER SENSITIVE BACKUPS ARE DONE FOR: /Projects
pn_BIOMAG=/BIOMAG_DATA
pn_projects=$pn_BIOMAG/Projects
pn_backup=/mnt/dresden/BACKUP_BIOMAG/BIOMAG_DATA
pn_backup_projects=$pn_backup/Projects
start=`date +%s`
# #COMPLETE BACKUPS ARE DONE FOR: /STORAGE, /LIB, /scripts
RSYNC=();
RSYNC+=("rsync -avP $pn_BIOMAG/STORAGE/ $pn_backup/STORAGE/");
RSYNC+=("rsync -avP $pn_BIOMAG/LIB/ $pn_backup/LIB/");
RSYNC+=("rsync -avP $pn_BIOMAG/scripts/ $pn_backup/scripts/");

# #PROJETS
DIRS=('code' 'docs' 'data/processed_final' 'results/figures' 'results/important_results');

if [ ! -d $pn_backup_projects ]; then
  	RSYNC+=("mkdir -p $pn_backup_projects");
fi

for pn in $(find $pn_projects -mindepth 1 -maxdepth 1 -type d)
do
	#first create the PROJECT FOLDER
	new_pn_project=`basename "$pn"`
	new_pn_project=$pn_backup_projects/$new_pn_project
	if [ ! -d $new_pn_project ]; then
		RSYNC+=("mkdir -p $new_pn_project")
	fi

	#SECOND: add the copy rootdir
	RSYNC+=("cp -v $pn/* $new_pn_project/")

	#THIRD: loop through dirs and add them
	for i in "${DIRS[@]}"; 
	do  
		from_dir="$pn/$i/"
		to_dir="$new_pn_project/$i/"
        	if [ ! -d $to_dir ]; then
                	RSYNC+=("mkdir -p $to_dir")
        	fi
		RSYNC+=("rsync -avP $from_dir $to_dir")
	done

done

## print the RSYNC command
echo "Starte BACKUP: $pn_BIOMAG => $pn_backup"
for i in "${!RSYNC[@]}"; 
do
	cmd="${RSYNC[$i]}"
	echo "$(($i+1))/${#RSYNC[@]}: $cmd"; 
	$cmd
done

## FERTIG
end=`date +%s`
runtime=$(python -c "print(${end} - ${start})")
echo "FERTIG :-)	DAUER: $runtime"

echo "last backup:  $(date)" >> /BIOMAG_DATA/.last_backup_biomag.log

