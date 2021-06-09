#!/usr/bin/python

# pm_series_get.py
# Ermöglicht das Laden einer Serie aus einer notion Datenbank anhand seiner ID in ein Projekt
# Der Ordnername bestehe dabei aus: [suffix (optional)]_Subject_tags
# usage: 
#   + Hilfe: pm_series_get
#   + DEMO: pm_series_get DEMO
#   + anwendung: pm_series_get NOTION-ID PROJECT_FOLDER [opt: suffix]
#   + bsp: pm_series_get 4f40fa57-a49a-4b95-8b0a-8243155cb9a9 /opt/biomag-db/py-manager/DEMO/sample_project
#   + bsp: pm_series_get 4f40fa57-a49a-4b95-8b0a-8243155cb9a9 /opt/biomag-db/py-manager/DEMO/sample_project test

from pm_notion_api import *
import os
import sys
import json

print('pm_series_get (v0.2):', 'argumente: ', len(sys.argv))

if len(sys.argv) < 3: 
    print('+ usage/help:')
    print('++ pm_series_get ID  Projekt')
    print('  oder')
    print('++ pm_series_get ID Projekt suffix')
    print('   ID - notion ID eines eintrages')
    print('   target_project_dir: Projektname (im BIOMAG/ Verzeichnis)')
    print('   suffix: optionaler Suffix f. den Unterordner der Daten, Standard ist: [leer]')

    sys.exit(0)

# LOAD THE PRESETS
with open(os.path.join(os.path.dirname(__file__), 'pm_settings.json')) as f:
    presets = json.load(f)

if len(sys.argv) == 4:
    suffix = "%s_%s" % (sys.argv[3].rstrip(), '_')
else:
    suffix = ''


# INIT THE DATA
if sys.argv[1] != 'DEMO':
    notion_id = sys.argv[1]
    project_name = sys.argv[2]
else: 
    print('DEMO')
    project_name = 'DEMO_PROJECT'
    notion_id = presets['demo_id']

if not os.path.exists(os.path.join(presets['project_root_dir'], project_name)): 
    print('Projekt nicht gefunden: ' + project_name)
    print('bitte neu anlegen mit: pm_project_create', project_name)
    sys.exit(0)

DATA_DIR = os.path.join(presets['storage_dir'], notion_id)
if not os.path.exists(DATA_DIR): 
    print('ID nicht gefunden: ' + notion_id)
    sys.exit(0)

#Ordner wurden gefunden
files = os.listdir(DATA_DIR)
if len(files) == 0:
    print('Datenverzeichnis ist leer: {}'.format(DATA_DIR))
    sys.exit(0)

print('+ id = ', notion_id)
print('+ gefunden: ', files)

PROJECT_DIR = os.path.join(presets['project_root_dir'], project_name, 'data', 'raw')
list = os.listdir(PROJECT_DIR)
for x in list:
    if os.path.isdir(os.path.join(PROJECT_DIR, x)):
        # try to read the json in the existing folder
        meta_file = os.path.join(PROJECT_DIR,x, 'meta.json')
        if os.path.isfile(meta_file):
            with open(meta_file) as f:
                meta_info = json.load(f)
                if meta_info['id'] == notion_id:
                    print('ID ', notion_id, ' bereits importiert: ', os.path.join(PROJECT_DIR, x))
                    answer = input('Fortfahren (ja / nein): ')
                    if len(answer) == 0 or answer[0].lower() != 'j':
                        print('abgebrochen')
                        sys.exit(0) 

#connecto to notion and get the subject name
print('+ öffne Verbindung zu NOTION')
nsync = NotionSync()
res = nsync.get_entry({"NID": notion_id})
# print(res)

print('+++ erfolgreich')
folder_name = suffix.rstrip()
if res["Subject"] != None and len(res["Subject"]) > 0:
    TITLE=res["Subject"];
else:
    print('kein SUBJECT gefunden, nutze [description] als TITLE')
    TITLE=res["description"];

folder_name="%s%s" % (suffix.rstrip(), TITLE)

if res.get("measure_number") is None:
    print('measure_number muss definiert sein!!!')
    sys.exit(0)
rep= res["measure_number"]

folder_name = "%s__%i" % (folder_name.rstrip(), rep)

#CHECKE DAS VERZIECHNIS
WRITE_DIR = os.path.join(PROJECT_DIR, folder_name.rstrip())
SUBJ_IND = 0;
while os.path.exists(WRITE_DIR):
    SUBJ_IND = SUBJ_IND + 1
    WRITE_DIR = os.path.join(PROJECT_DIR, "%s_%i" % (folder_name.rstrip(), SUBJ_IND))

#ERSTELLE das VERZEICHNIS
print('+ erstelle: ', WRITE_DIR)
os.makedirs(WRITE_DIR)

with open(os.path.join(WRITE_DIR, 'meta.json'), 'w') as outfile:
        json.dump({'id': notion_id, 'path': WRITE_DIR}, outfile)

for file in files:
    if file != 'meta.json':
        print('++ erstelle symlink: ', file)
        os.symlink(os.path.join(DATA_DIR, file), os.path.join(WRITE_DIR, file))

print('fertig :-)')
