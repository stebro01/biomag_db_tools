#!/bin/bash
QUOTA=/BIOMAG_DATA/.quota.log


echo "last run:  $(date)" > $QUOTA

echo "/home:" >> $QUOTA
du -hs /home/* >> $QUOTA

echo "/BIOMAG_DATA:" >> $QUOTA
du -hs /BIOMAG_DATA/* >> $QUOTA

echo "/mnt/dresden/BACKUP_BIOMAG:" >> $QUOTA
du -hs /mnt/dresden/BACKUP_BIOMAG/* >> $QUOTA

echo "/mnt/dresden/BACKUP_TSKI:" >> $QUOTA
du -hs /mnt/dresden/BACKUP_TSKI/* >> $QUOTA

echo "/mnt/R:" >> $QUOTA
du -hs /mnt/R/* >> $QUOTA

echo "/mnt/Q:" >> $QUOTA
du -hs /mnt/Q/* >> $QUOTA
