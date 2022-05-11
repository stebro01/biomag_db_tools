#!/bin/bash
#dieses SKRIPT sorgt dafuer, dass im Storage daten nur gelesen werden koennen
DIR=/BIOMAG_DATA/STORAGE

echo Aendere Rechte im Ordner: $DIR zu 555

chown -R ste:users $DIR/*

chmod -R 555 *
chmod 775 $DIR

echo FERTIG
echo
