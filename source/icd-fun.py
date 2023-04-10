""" 
ICD functions
functions for the alfred-ICDbrowser workflow
Sunny ☀️   🌡️+59°F (feels +59°F, 26%) 🌬️→6mph 🌖&m Mon Apr 10 14:02:51 2023
W15Q2 – 100 ➡️ 264 – 334 ❇️ 30

"""



from config import  MY_DATAFILE, log
import pandas as pd

def createDatabase():
    # import the data file

    log ("reading data in ...")
    df = pd.read_csv(MY_DATAFILE)
    


def main():
    createDatabase()
    
    
    

if __name__ == '__main__':
    main ()
