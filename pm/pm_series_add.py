#!/usr/bin/python

# Soll einen Eintrag in Notion erstellen anhand: der Dateien im aktuellen Verzeichnis sowie der angegebenen Informationen, dies wird dann in notion gespeichert beziehungsweise die Dateien wären denn in den globalen Speicher/STORAGE kopiert
# https://www.notion.so/8bb0af001f5d440994247d5b5d5166c5?v=360cedf4505e4130b43e97db6104bec3

# pm_series_add.py
# Speichert Daten aus einem Ordner in die Datenbank (NOTION & lokaler Storage)
# KONVENTION: keine SUBFOLDER, alle Dateien im Ordner werden hinzugefügt und verschoben
# usage: 
#   + Hilfe: pm_series_add
#   + DEMO: pm_series_add DEMO
#   + anwendung: pm_series_add NOTION-ID STORAGE_FOLDER PROJECT_FOLDER [opt: suffix]

from pm_notion_api import *
import os
import shutil
import json
import sys

print('pm_series_add (v0.1):', 'argumente: ', len(sys.argv))


def save_to_notion(presets, meta, data_dir, files, modus):
    print('+ öffne Verbindung zu NOTION')
    nsync = NotionSync()
    meta["status"] = "schreibe"
    meta["files"] = files
    status_id = nsync.add_entry(meta)

    print('+ UPDATE PFAD')
    OUT_DIR = os.path.join(presets['storage_dir'], status_id)
    nsync.update_entry(status_id, {"absolute_path": OUT_DIR})

    # # VERSCHIEBE JETZT DIE DATEN
    print('+ verschiebe Daten in: {}'.format(OUT_DIR))
    result = move_files(data_dir, OUT_DIR, files)
    with open(os.path.join(OUT_DIR, 'meta.json'), 'w') as outfile:
        json.dump({'id': status_id,'description': meta, 'files': files, 'path': OUT_DIR}, outfile)
    if result == True:
        nsync.update_entry(status_id, {"status": "ok"})

        if modus == 'single':
            answer = input('Soll das Verzeichnis gelehrt&gelöscht werden? (ja/nein): ')
        else:
            answer = 'ja'

        if len(answer) > 0 and answer[0].lower() == 'j':
            shutil.rmtree(data_dir)
        else: 
            print('bitte das Verzeichnis ggf. manuell löschen: rmdir ', data_dir)
    
    print('fertig :-)')

# frage eine JSON entsprechend den werten in pm_settings > presets.db_schema ab / derzeit keine Erkennung des Types!
def query_meta(schema):
    data = schema
    for (k, v) in schema.items():
        data[k] = input(k+': ')
    return data

# Bewege die Dateien
def move_files(data_dir, OUT_DIR, files):
    if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)
    for fn in files:
        os.rename(os.path.join(data_dir, fn), os.path.join(OUT_DIR, fn))
    return True

if len(sys.argv) < 2:
    print('+ usage/help:')
    print('++   pm_series_add FOLDER_CONTAINING_DATA')

    sys.exit(0)

# LOAD THE PRESETS
with open(os.path.join(os.path.dirname(__file__), 'pm_settings.json')) as f:
    presets = json.load(f)

# DATA?
if sys.argv[1] == 'DEMO':
    data_dir = presets['demo_data_dir']
else:
    data_dir = sys.argv[1]

storage_dir = presets['storage_dir']
print('STORAGE gefunden: ', storage_dir)

if not os.path.exists(storage_dir):
    os.makedirs(storage_dir)
#check the data_folder
if not os.path.exists(data_dir):
    print('nicht gefunden: {}'.format(data_dir))
    sys.exit(0)

files = os.listdir(data_dir)
if len(files) == 0:
    print('Datenverzeichnis ist leer: {}'.format(data_dir))
    sys.exit(0)

print('Dateien gefunden: ')
print(files)

if len(sys.argv) == 2:
    # FRAGE
    answer = input('Verschiebe Dateien in den Storage? (ja / nein): ')
    if len(answer) == 0 or answer[0].lower() != 'j':
        sys.exit(0) 

    #erfrage meta data
    meta = query_meta(presets['db_schema'])
    modus = 'single'
else:
    meta = {}
    modus = 'multiple'
    if len(sys.argv) >= 3:
        meta['description'] = sys.argv[2]
    if len(sys.argv) >= 4:
        meta['notes'] = sys.argv[3]


# speichere in NOTION
save_to_notion(presets, meta, data_dir, files, modus)
