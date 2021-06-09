import string
import random
import sys
import os
import json
from pm_notion_api import *

print('pm_subject_random_id (v0.1):', 'argumente: ', len(sys.argv))

def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def firstRun(id, fn):
    print('neue ID: ', id)
    print(' wird gespeichert in => ', fn)
    outdata = []
    outdata.append(id)
    with open(fn, 'w') as outfile:
        json.dump({'subject_ids': outdata}, outfile)
        

def addToNotion(id):
    print('     Adding to notion ...')
    # LOAD THE PRESETS
    with open(os.path.join(os.path.dirname(__file__), 'pm_settings.json')) as f:
        presets = json.load(f)
    # open notion 
    nsync = NotionSync()
    nsync.add_entry({"subject_id": id, "database_id": "05eba3dbce8c4cf5b9ea8d62bcd28c7a"})
    print('     done')

SAVE_FN = os.path.join(os.path.dirname(__file__), 'pm_subject_random_id.json')
if os.path.exists(SAVE_FN):
    print('Checking existing id list in: ', SAVE_FN)
    firstRUN = False
else:
    print('First run')
    firstRUN = True

#is firstRUN?
if firstRUN:
    subject_id = id_generator()
    firstRun(subject_id, SAVE_FN)
    addToNotion(subject_id)
    sys.exit(0)

# load the ids already given
with open(SAVE_FN,) as infile:
    data  = json.load(infile)
given_ids = data['subject_ids']

# create the ID
new_id_found = False

while new_id_found == False:
    subject_id = id_generator()
    if subject_id not in given_ids:
        new_id_found = True

print('Neue ID: ', subject_id)
given_ids.append(subject_id)
# wird gespeichert
print(' speichere in: ', SAVE_FN, '(', str(len(given_ids)), 'Einträge)')
with open(SAVE_FN, 'w') as outfile:
    json.dump({'subject_ids': given_ids}, outfile)

addToNotion(subject_id)