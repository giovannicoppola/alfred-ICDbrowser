""" 
ICD query
a query script for the alfred-ICDbrowser workflow
Sunny ☀️   🌡️+53°F (feels +51°F, 38%) 🌬️→2mph 🌖&m Tue Apr 11 08:59:58 2023
W15Q2 – 101 ➡️ 263 – 335 ❇️ 29

"""

from config import  log, DATABASE_FILE
import pandas as pd
import sqlite3
import sys
import json
import os

MYINPUT = sys.argv[1].casefold().strip()
MY_LEVEL = int(os.getenv('mySource')) if os.getenv('mySource') else 1
MY_NODE = int(os.getenv('myNode')) if os.getenv('myNode') else 0
MY_MASTER_ID = int(os.getenv('myMasterID')) if os.getenv('myMasterID') else 0
BACKUPID = int(os.getenv('backupID')) if os.getenv('backupID') else 0
KEYCAPS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]

def icdQuery(MYINPUT):
    db = sqlite3.connect(DATABASE_FILE)
    db.row_factory = sqlite3.Row
    myCounter = 0
    allFlag = 0

    if "--a" in MYINPUT:

        MYINPUT = MYINPUT.replace ('--a','').strip()
        allFlag = 1


    myNode = f"nodeL{MY_LEVEL-1}"
        
    
    if MY_LEVEL == 1:
        myNodeStr = ""
    else:
        myNodeStr = f"AND {myNode} LIKE {MY_NODE}"
    keywords = MYINPUT.split()
    if len(keywords) > 1:
        conditions = []
        
        for keyword in keywords:
            conditions.append(f"(description LIKE '%{keyword}%')")
            conditions_str = " AND ".join(conditions)
    else:
        conditions_str = (f"(description LIKE '%{MYINPUT}%')")
        

    # getting list of tags from the database
    if allFlag == 1:
        sql_statement = f"SELECT * FROM ICDnew WHERE {conditions_str} {myNodeStr} ORDER BY children DESC"
    else:
        sql_statement = f"SELECT * FROM ICDnew WHERE level like {MY_LEVEL} AND {conditions_str} {myNodeStr} ORDER BY itemID"
    log (sql_statement)
    rs = db.execute(sql_statement).fetchall()
    
    result = {"items": [], "variables":{}}
    if rs: 
    
        totCount = len(rs)
        myCounter = 0
        #initializing JSON output
        
        
        for r in rs:
            myCounter += 1
            if MY_LEVEL > 2:
                upNoDe = f'nodeL{MY_LEVEL-2}'
                upNoDe1 = f'nodeL{MY_LEVEL-1}'
            else:
                upNoDe = f'nodeL1'
                upNoDe1 = f'nodeL1'
            
                
            result["items"].append({
                        "title": f"{KEYCAPS[r['level']]} {r['name']}: {r['description']} (⤵️ {r['children']})",
                        
                        'subtitle': f"{myCounter}/{totCount} – level: {r['level']}",
                        'valid': True,
                        'variables': {
                            "mySource": r['level'] + 1,
                            "myNode": r[1],
                            "backupID": r[upNoDe1]
                        },
                        "mods": {
                            "shift": {
                                "valid": True,
                                'variables': {
                                    "myTextOutput": f"{KEYCAPS[r['level']]} {r['name']}: {r['description']} (⤵️ {r['children']})"
                                    
                                        },
                                "arg": ""
                                
                            },
                            "ctrl": {
                                "valid": True,
                                'variables': {
                                    "mySource": 99, #source for fetchHierarchy
                                    "myMasterID": r['masterID']
                                        },
                                "arg": "",
                                "subtitle": "show in hierarchy"
                            },
                            "cmd": {
                                "valid": True,
                                "arg": "",
                                'variables': {
                                    "mySource": r['level'] - 1,
                                        "myNode": r[upNoDe]
                                    },
                                "subtitle": "⬅️ back"
                            }
                        },
                        "icon": {
                        "path": f"icons/{r['chapter']}.png",
                        },
                        'arg': r[1]
                            }) 
    else: 
        result["items"].append({
        "title": "No matches at this level. Enter ↩️ to go back",
        
        "subtitle": "⬅️ back",
        'variables': {
                                    "mySource": MY_LEVEL - 1,
                                        "myNode": BACKUPID
                                    },
         "mods": {
                           
                            "cmd": {
                                "valid": True,
                                "arg": "",
                                'variables': {
                                           "mySource": MY_LEVEL - 1,
                                        "myNode": BACKUPID
                             },
                                "subtitle": "⬅️ back"
                            }
                        },
        "arg": "",
        "icon": {
            "path": "icons/Warning.png"
            }
        
            })

    if MYINPUT and not rs:
        result["items"].append({
        "title": "No matches in your library",
        "subtitle": "Try a different query",
        "arg": "",
        "icon": {
            "path": "icons/Warning.png"
            }
        
            })

    print (json.dumps(result))
                


def fetchHierarchy (masterID):
    myTextOutput = ''
    db = sqlite3.connect(DATABASE_FILE)
    db.row_factory = sqlite3.Row
    
    sql_statement = f"SELECT * FROM ICDnew WHERE masterID LIKE {masterID}"
    rs = db.execute(sql_statement).fetchone()
    result = {"items": [], "variables":{}}
    
    for myLevel in range(1,rs['level']+1):
        
        if myLevel == rs['level']:
            currNode = rs['masterID']
            probandIcon = '✴️'
        else:
            currNodeLevel = f"nodeL{myLevel}"
            currNode = rs[currNodeLevel]
            probandIcon = ''
        
        currTabs = "\t" * (myLevel-1)
        
        
        l1 = db.execute(f"SELECT * FROM ICDnew WHERE masterID LIKE {currNode}").fetchone()
        result["items"].append({
            "title": f"{currTabs}{KEYCAPS[myLevel]}{l1['name']}: {l1['description']} (⤵️ {l1['children']}) {probandIcon}",
            
            'subtitle': f"{myLevel}/{rs['level']} {l1['description']} mySource: {MY_LEVEL} myNode: {l1[1]}, level: {l1['level']}",
            'valid': True,
            'variables': {
                "mySource": l1['level'] + 1,
                "myNode": l1[1]
            },
            
            "icon": {
            "path": f"icons/{l1['chapter']}.png",
            },
            'arg': l1[1]
                }) 
        myTextOutput = myTextOutput + f"\n{currTabs}{l1['level']}.{l1['name']}: {l1['description']} (>{l1['children']}) {probandIcon}"
    result['variables'] = {"myTextOutput": myTextOutput}   
    print (json.dumps(result))



def main():
    
    if MY_LEVEL == 99:
        fetchHierarchy (MY_MASTER_ID)
    else:
        icdQuery(MYINPUT)
    
    
    

if __name__ == '__main__':
    main ()
