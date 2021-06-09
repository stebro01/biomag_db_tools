# Erstellt ein leeres Projekt anhand eines schemas >> das kann perspektivisch auch aus notion kommen

import os
import sys
import json

print('pm_project_create (v0.1):', 'argumente: ', len(sys.argv))

# http://handbook.datalad.org/en/latest/basics/101-127-yoda.html


def create_dir(OUT_DIR, txt):
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    with open(os.path.join(OUT_DIR, 'meta.json'), 'w') as outfile:
        json.dump({'info': txt, 'path': OUT_DIR}, outfile)
    

def loop_items(ITEM, pn):
    for k,v in ITEM.items():
        OUT_DIR = os.path.join(pn, k)
        if isinstance(v, str):
            print('+ Erzeuge Unterverzeichnisse: ' + OUT_DIR)
            create_dir(OUT_DIR, v)
        else:
            loop_items(v, OUT_DIR)


# CLI Arguments
if len(sys.argv) < 2:
    print('+ usage/help')
    print('++ pm_project_create PROJECT_NAME')
    sys.exit(0)

# READ ARGUMENTS
if sys.argv[1] == 'DEMO':
    project_name = 'DEMO_PROJECT'
else:   
    project_name = sys.argv[1]

# LOAD THE PRESETS
with open(os.path.join(os.path.dirname(__file__), 'pm_settings.json')) as f:
    presets = json.load(f)

# CHECKE DEN PFAD
project_root_folder = presets['project_root_dir']

OUT_DIR = os.path.join(project_root_folder, project_name)
if os.path.exists(OUT_DIR):
    print('Projekt existiert schon: ' + OUT_DIR)
    sys.exit(0)


print('neues Projekt: ', OUT_DIR)
answer = input('Soll dieses Projekt angelegt werden? (ja / nein) ')

if len(answer) == 0 or answer[0].lower() != 'j':
    sys.exit(0) 

# ERZEUGE JETZT DAS PROJEKT
print('Erzeuge Projekt-Verzeichnis: '+OUT_DIR)
create_dir(OUT_DIR, 'leeres Projekt')
loop_items(presets['project_schema'], OUT_DIR)

print('fertig')