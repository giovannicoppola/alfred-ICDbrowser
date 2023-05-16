""" 
ICD functions
functions for the alfred-ICDbrowser workflow
Sunny ☀️   🌡️+59°F (feels +59°F, 26%) 🌬️→6mph 🌖&m Mon Apr 10 14:02:51 2023
W15Q2 – 100 ➡️ 264 – 334 ❇️ 30

"""

import pandas as pd
import sqlite3
import xmltodict
import json
import sys

myXMLfile = sys.argv[1]

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


def CSVtoSQL(myCSVData,myDatabase):
    # read in the data file

    log ("reading data in ...")
    df = pd.read_csv(myCSVData)
    print (df.info())
    con = sqlite3.connect(myDatabase)
    cursor = con.cursor()
    
    # level 1
    level1 = df.drop_duplicates(subset=['meaning_L1'], keep='first')[['meaning_L1','node_L1']]
    print (f"1. creating the level1 database table", end = "...")
    level1['key'] = range(1, len(level1.index)+1)
    cursor.execute(f"DROP TABLE IF EXISTS level1")
    level1.to_sql('level1', con, index=False) 
    print ("done")
    

# level 2
    level2 = df.drop_duplicates(subset=['meaning_L2'], keep='first')[['meaning_L2','node_L2','node_L1']]
    print (f"1. creating the level1 database table", end = "...")
    level2['key'] = range(1, len(level2.index)+1)
    cursor.execute(f"DROP TABLE IF EXISTS level2")
    
    level2.to_sql('level2', con, index=False) 
    print ("done")
    

# level 3
    level3 = df.drop_duplicates(subset=['meaning_L3'], keep='first')[['meaning_L3','node_L3','node_L2','node_L1']]
    print (f"1. creating the level1 database table", end = "...")
    level3['key'] = range(1, len(level3.index)+1)
    cursor.execute(f"DROP TABLE IF EXISTS level3")
    level3.to_sql('level3', con, index=False) 
    print ("done")
    
# level 4
    level4 = df.drop_duplicates(subset=['meaning_L4'], keep='first')[['meaning_L4','node_L4','node_L3','node_L2','node_L1']]
    print (f"1. creating the level1 database table", end = "...")
    level4['key'] = range(1, len(level4.index)+1)
    cursor.execute(f"DROP TABLE IF EXISTS level4")
    level4.to_sql('level4', con, index=False) 
    print ("done")

# level 5
    level5 = df.drop_duplicates(subset=['meaning_L5'], keep='first')[['meaning_L5','node_L5','node_L4','node_L3','node_L2','node_L1']]
    print (f"1. creating the level1 database table", end = "...")
    level5.dropna(subset=['meaning_L5'], inplace=True)
    level5['key'] = range(1, len(level5.index)+1)
    cursor.execute(f"DROP TABLE IF EXISTS level5")
    
    level5.to_sql('level5', con, index=False) 
    print ("done")

def XMLtoJSON(myFile,myOutputFile):

    # Read the XML file
    with open(myFile, 'r') as file:
    #with open(myFile, 'r', encoding='iso-8859-1') as file:
        xml_data = file.read()

    # Convert the XML to a Python dictionary
    dict_data = xmltodict.parse(xml_data)

    # Convert the dictionary to JSON
    json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)

    # Save the JSON to a file
    with open(myOutputFile, 'w') as file:
        file.write(json_data)
    return json_data

def flattenJSON (myDataFile, myDatabase):
    with open(myDataFile) as f:
        myData = json.load(f)
    
    
    myData = myData["ICD10CM.tabular"]['chapter']
    chapterCount = 0
    masterCount = 0
    ICDlist = [] 
    ICDdict = {}

    l1N = len (myData) # total number of chapters (L1, letters)
    ### Level 1 (main 22 groups)
    for myChapter in myData:
        chapterCount += 1
        
        level2G = len (myChapter['section']) # number of L2 groups
        
        masterCount += 1
        ### ADDING TO ICD LIST
        ICDdict = {
            'level': 1,
            'masterID': masterCount,
            'chapter': chapterCount,
            'itemID': chapterCount,
            'itemIDprog': f"{chapterCount}/{l1N}",
            'name': myChapter['name'],
            'description': myChapter['desc'],
            'children': level2G
        }
        ICDlist.append(ICDdict)
        ######## 


        if chapterCount == 7:
            print (f"{chapterCount}/{l1N}: {myChapter['desc']}, has {level2G} L2 groups")
        l2G = 0
        
        ### Level 2 GROUPS
        # `section` can be a list or dict
        parentID = masterCount
        if isinstance (myChapter['section'],list): # going through the level 2 groups
            for myLevel2Group in myChapter['section']:
                l2G += 1
                
                
                
                ### Level 2 ITEMS
                if 'diag' in myLevel2Group and isinstance (myLevel2Group['diag'],list):
                    level2N = len (myLevel2Group['diag'])
                    
                    masterCount += 1
                    ### ADDING TO ICD LIST, LEVEL 2
                    ICDdict = {
                        'level': 2,
                        'nodeL1': parentID,
                        'masterID': masterCount,
                        'chapter': chapterCount,
                        'itemID': l2G,
                        'itemIDprog': f"{l2G}/{level2G}",
                        'name': myLevel2Group['@id'],
                        'description': myLevel2Group['desc'],
                        'children': level2N
                    }
                    ICDlist.append(ICDdict)
                    ######## 

                    if chapterCount == 7:
                        print (f"\t {l2G}/{level2G} group: {myLevel2Group['desc']}, {level2N} L2 items")

                    l2C = 0
                    parentID2 = masterCount
                    for myLevel2item in myLevel2Group['diag']: # going through the L2 items
                        l2C += 1
                        
                        
                        ### Level 3
                        if 'diag' in myLevel2item and isinstance (myLevel2item['diag'],list):
                            l3C =0
                            level3N = len (myLevel2item['diag'])
                            
                            masterCount += 1
                            ### ADDING TO ICD LIST, LEVEL 3
                            ICDdict = {
                                'level': 3,
                                'nodeL1': parentID,
                                'nodeL2': parentID2,
                                'masterID': masterCount,
                                'chapter': chapterCount,
                                'itemID': l2C,
                                'itemIDprog': f"{l2C}/{level2N}",
                                'name': myLevel2item['name'],
                                'description': myLevel2item['desc'],
                                'children': level3N
                            }
                            ICDlist.append(ICDdict)
                            ######## 
                            if chapterCount == 7:
                                print (f"\t\t {l2C}/{level2N} {myLevel2item['name']}: {myLevel2item['desc']}, {level3N} L3 children")

                            parentID3 = masterCount
                            for myLevel3 in myLevel2item['diag']: #going through the level3 items
                                l3C += 1
                                
                                
                                
                                # level 4
                                if 'diag' in myLevel3 and isinstance (myLevel3['diag'],list):
                                    l4C =0
                                    level4N = len (myLevel3['diag'])
                                    
                                    masterCount += 1
                                    ### ADDING TO ICD LIST, LEVEL 4
                                    ICDdict = {
                                        'level': 4,
                                        'nodeL1': parentID,
                                        'nodeL2': parentID2,
                                        'nodeL3': parentID3,
                                        'masterID': masterCount,
                                        'chapter': chapterCount,
                                        'itemID': l3C,
                                        'itemIDprog': f"{l3C}/{level3N}",
                                        'name': myLevel3['name'],
                                        'description': myLevel3['desc'],
                                        'children': level4N
                                    }
                                    ICDlist.append(ICDdict)
                                    ######## 

                                    if chapterCount == 7:
                                        print (f"\t\t\t {l3C}/{level3N}: {myLevel3['name']}: {myLevel3['desc']}, {level4N} L4 children")
                                    
                                    parentID4 = masterCount
                                    for myLevel4 in myLevel3['diag']: #going through the level4 items
                                        l4C += 1
                                        
                                        if 'diag' in myLevel4 and isinstance (myLevel4['diag'],list):
                                            l5C =0
                                            level5N = len (myLevel4['diag'])
                                            
                                            masterCount += 1
                                            
                                            ### ADDING TO ICD LIST, LEVEL 5
                                            ICDdict = {
                                                'level': 5,
                                                'nodeL1': parentID,
                                                'nodeL2': parentID2,
                                                'nodeL3': parentID3,
                                                'nodeL4': parentID4,
                                                'masterID': masterCount,
                                                'chapter': chapterCount,
                                                'itemID': l4C,
                                                'itemIDprog': f"{l4C}/{level4N}",
                                                'name': myLevel4['name'],
                                                'description': myLevel4['desc'],
                                                'children': level5N
                                            }
                                            ICDlist.append(ICDdict)
                                            ######## 


                                            if chapterCount == 7:
                                                print (f"\t\t\t\t {l4C}/{level4N}: {myLevel4['name']}: {myLevel4['desc']}, {level5N} L5 children")    
                                            
                                            # level 5
                                            parentID5 = masterCount
                                            for myLevel5 in myLevel4['diag']: #going through the level5 items
                                                l5C += 1
                                                if 'diag' in myLevel5 and isinstance (myLevel5['diag'],list):
                                                    l5C =0
                                                    level6N = len (myLevel5['diag'])
                                                    
                                                    masterCount += 1
                                                    
                                                    ### ADDING TO ICD LIST, LEVEL 6
                                                    ICDdict = {
                                                        'level': 6,
                                                        'nodeL1': parentID,
                                                        'nodeL2': parentID2,
                                                        'nodeL3': parentID3,
                                                        'nodeL4': parentID4,
                                                        'nodeL5': parentID5,
                                                        'masterID': masterCount,
                                                        'chapter': chapterCount,
                                                        'itemID': l5C,
                                                        'itemIDprog': f"{l5C}/{level5N}",
                                                        'name': myLevel5['name'],
                                                        'description': myLevel5['desc'],
                                                        'children': level6N
                                                    }
                                                    ICDlist.append(ICDdict)
                                                    ######## 

                                                    if chapterCount == 7:
                                                        print (f"\t\t\t\t\t {l5C}/{level5N}: {myLevel5['name']}: {myLevel5['desc']} {level6N} L6 children")    
                                                
                                                elif 'diag' in myLevel5: #diag is in level5, but not a list:
                                                    level6N = 0
                                                    
                                                    masterCount += 1
                                                    ### ADDING TO ICD LIST, LEVEL 6
                                                    ICDdict = {
                                                        'level': 6,
                                                        'nodeL1': parentID,
                                                        'nodeL2': parentID2,
                                                        'nodeL3': parentID3,
                                                        'nodeL4': parentID4,
                                                        'nodeL5': parentID5,
                                                        'masterID': masterCount,
                                                        'chapter': chapterCount,
                                                        'itemID': l5C,
                                                        'itemIDprog': f"{l5C}/{level5N}",
                                                        'name': myLevel5['diag']['name'],
                                                        'description': myLevel5['diag']['desc'],
                                                        'children': level6N
                                                    }
                                                    ICDlist.append(ICDdict)
                                                    ######## 

                                                    if chapterCount == 7:
                                                        print (f"\t\t\t\t\t {l5C}/{level5N}: {myLevel5['diag']['name']}: {myLevel5['diag']['desc']}, {level6N} L6 children")   
                                                else: # no diag in item
                                                    level6N = 0
                                            
                                                    masterCount += 1
                                                    ### ADDING TO ICD LIST, LEVEL 6
                                                    ICDdict = {
                                                        'level': 6,
                                                        'nodeL1': parentID,
                                                        'nodeL2': parentID2,
                                                        'nodeL3': parentID3,
                                                        'nodeL4': parentID4,
                                                        'nodeL5': parentID5,
                                                        'masterID': masterCount,
                                                        'chapter': chapterCount,
                                                        'itemID': l5C,
                                                        'itemIDprog': f"{l5C}/{level5N}",
                                                        'name': myLevel5['name'],
                                                        'description': myLevel5['desc'],
                                                        'children': level6N
                                                    }
                                                    ICDlist.append(ICDdict)
                                                    ######## 
                                                    if chapterCount == 7:
                                                        print (f"\t\t\t\t\t {l5C}/{level5N}: {myLevel5['name']}: {myLevel5['desc']}, {level6N} L6 children")   
                                        
                                        elif 'diag' in myLevel4: #diag is in level4, but not a list:
                                            level5N = 0
                                            
                                            masterCount += 1
                                            ### ADDING TO ICD LIST, LEVEL 5
                                            ICDdict = {
                                                'level': 5,
                                                'nodeL1': parentID,
                                                'nodeL2': parentID2,
                                                'nodeL3': parentID3,
                                                'nodeL4': parentID4,
                                                'masterID': masterCount,
                                                'chapter': chapterCount,
                                                'itemID': l4C,
                                                'itemIDprog': f"{l4C}/{level4N}",
                                                'name': myLevel4['diag']['name'],
                                                'description': myLevel4['diag']['desc'],
                                                'children': level5N
                                            }
                                            ICDlist.append(ICDdict)
                                            ######## 

                                            if chapterCount == 7:
                                                print (f"\t\t\t\t {l4C}/{level4N}: {myLevel4['diag']['name']}: {myLevel4['diag']['desc']}, {level5N} L5 children")    
                                        
                                        
                                        else: # no diag in item
                                            level5N = 0
                                            
                                            masterCount += 1
                                            ### ADDING TO ICD LIST, LEVEL 5
                                            ICDdict = {
                                                'level': 5,
                                                'nodeL1': parentID,
                                                'nodeL2': parentID2,
                                                'nodeL3': parentID3,
                                                'nodeL4': parentID4,
                                                'masterID': masterCount,
                                                'chapter': chapterCount,
                                                'itemID': l4C,
                                                'itemIDprog': f"{l4C}/{level4N}",
                                                'name': myLevel4['name'],
                                                'description': myLevel4['desc'],
                                                'children': level5N
                                            }
                                            ICDlist.append(ICDdict)
                                            ######## 

                                            if chapterCount == 7:
                                                print (f"\t\t\t\t {l4C}/{level4N}: {myLevel4['name']}: {myLevel4['desc']}, {level5N} L5 children")    
                                
                                elif 'diag' in myLevel3: #diag is in level3, but not a list:
                                    level4N = 0
                                    
                                    masterCount += 1
                                    ### ADDING TO ICD LIST, LEVEL 4
                                    ICDdict = {
                                        'level': 4,
                                        'nodeL1': parentID,
                                        'nodeL2': parentID2,
                                        'nodeL3': parentID3,
                                        'masterID': masterCount,
                                        'chapter': chapterCount,
                                        'itemID': l3C,
                                        'itemIDprog': f"{l3C}/{level3N}",
                                        'name': myLevel3['diag']['name'],
                                        'description': myLevel3['diag']['desc'],
                                        'children': level4N
                                    }
                                    ICDlist.append(ICDdict)
                                    ######## 
                                    if chapterCount == 7:
                                        print (f"\t\t\t {l3C}/{level3N}: {myLevel3['name']}: {myLevel3['desc']}, {level4N} L4 children")
                                else: # no diag in item
                                    ### ADDING TO ICD LIST, LEVEL 4
                                    level4N = 0
                                    
                                    masterCount += 1
                                    ICDdict = {
                                        'level': 4,
                                        'nodeL1': parentID,
                                        'nodeL2': parentID2,
                                        'nodeL3': parentID3,
                                        'masterID': masterCount,
                                        'chapter': chapterCount,
                                        'itemID': l3C,
                                        'itemIDprog': f"{l3C}/{level3N}",
                                        'name': myLevel3['name'],
                                        'description': myLevel3['desc'],
                                        'children': level4N
                                    }
                                    ICDlist.append(ICDdict)
                                    ######## 

                        elif 'diag' in myLevel2item: #diag is in level2 items, but not a list
                            level3N = 0
                            
                            masterCount += 1
                            ### ADDING TO ICD LIST, LEVEL 3
                            ICDdict = {
                                'level': 3,
                                'nodeL1': parentID,
                                'nodeL2': parentID2,
                                'masterID': masterCount,
                                'chapter': chapterCount,
                                'itemID': l2C,
                                'itemIDprog': f"{l2C}/{level2N}",
                                'name': myLevel2item['diag']['name'],
                                'description': myLevel2item['diag']['desc'],
                                'children': level3N
                            }
                            ICDlist.append(ICDdict)
                            ######## 
                            if chapterCount == 7:
                                print (f"\t\t {myLevel2item['diag']['name']}: {myLevel2item['diag']['desc']}, {level3N} L3 children")
                        else: # no diag in item
                            level3N = 0
                            
                            masterCount += 1
                            ### ADDING TO ICD LIST, LEVEL 3
                            ICDdict = {
                                'level': 3,
                                'nodeL1': parentID,
                                'nodeL2': parentID2,
                                'masterID': masterCount,
                                'chapter': chapterCount,
                                'itemID': l2C,
                                'itemIDprog': f"{l2C}/{level2N}",
                                'name': myLevel2item['name'],
                                'description': myLevel2item['desc'],
                                'children': level3N
                            }
                            ICDlist.append(ICDdict)
                            ######## 
                            if chapterCount == 7:
                                print (f"\t\t {l2C}/{level2N} {myLevel2item['name']}: {myLevel2item['desc']}, {level3N} L3 children")
                
                elif 'diag' in myLevel2Group: #if diag is present in l2 groups, but not a list
                    
                    # level 3
                    if 'diag' in myLevel2Group['diag'] and isinstance (myLevel2Group['diag']['diag'],list):
                        level2N = len (myLevel2Group['diag']['diag'])
                        
                        masterCount += 1
                        ### ADDING TO ICD LIST, LEVEL 2
                        ICDdict = {
                        'level': 2,
                        'nodeL1': parentID,
                        'masterID': masterCount,
                        'chapter': chapterCount,
                        'itemID': l2G,
                        'itemIDprog': f"{l2G}/{level2G}",
                        'name': myLevel2Group['@id'],
                        'description': myLevel2Group['desc'],
                        'children': level2N
                        }
                        ICDlist.append(ICDdict)
                        ######## 
                        
                        if chapterCount == 7:
                            print (f"\t {l2G}/{level2G} group: {myLevel2Group['diag']['name']}: {myLevel2Group['diag']['desc']}, {level2N} L2 items")
                    
                        for myLevel3 in myLevel2Group['diag']['diag']:

                            if chapterCount == 7:
                                print (f"\t\t\t {myLevel3['name']}: {myLevel3['desc']}")
                else: #no diag in group: left in so the total matches the children of level 1, but these are not informative and could be removed. 
                    
                    masterCount += 1
                    ### ADDING TO ICD LIST, LEVEL2
                    ICDdict = {
                    'level': 2,
                    'nodeL1': parentID,
                    'masterID': masterCount,
                    'chapter': chapterCount,
                    'itemID': l2G,
                    'itemIDprog': f"{l2G}/{level2G}",
                    'name': myLevel2Group['@id'],
                    'description': myLevel2Group['desc'],
                    'children': 0
                    }
                    ICDlist.append(ICDdict)
                    ######## 
                        
                    if chapterCount == 7:
                        print (f"\t\t {myLevel2Group['name']}: {myLevel2Group['desc']}")
                
        else:
            # if section is not a list:
            # there is currently only one in this category, not imported:
            # `Provisional assignment of new diseases of uncertain etiology or emergency use (U00-U49), not a list`
            
            if chapterCount == 7:
                print (f"\t {myChapter['section']['desc']}, not a list")
            
    df = pd.DataFrame(ICDlist)
    
    df['nodeL1'] = df['nodeL1'].fillna(0).astype(int)
    df['nodeL2'] = df['nodeL2'].fillna(0).astype(int)
    df['nodeL3'] = df['nodeL3'].fillna(0).astype(int)
    df['nodeL4'] = df['nodeL4'].fillna(0).astype(int)
    df['nodeL5'] = df['nodeL5'].fillna(0).astype(int)
    
    con = sqlite3.connect(myDatabase)
    cursor = con.cursor()
    
    cursor.execute(f"DROP TABLE IF EXISTS ICDnew")
    df.to_sql('ICDnew', con, index=False) 
#    print (df.info())
    
    
    

def main():
    # convert from XML to JSON
    XMLtoJSON (myXMLfile,'icd-tabular.json')
    
    # flatten JSON to sqlite database
    flattenJSON ('icd-tabular.json', 'icd.db')
  

if __name__ == '__main__':
    main ()
