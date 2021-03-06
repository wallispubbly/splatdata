print ("SOMETHING IS BAD")

import requests
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
import os
import SplatoonResult

print("ATTEMPTING...")

load_dotenv()

def makeRequest():
    url = "https://app.splatoon2.nintendo.net/api/results"

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.1; SCH-I545 Build/LRX22C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36',
    'cookie': os.getenv("COOKIE")
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.status_code)
    return response.json()

def writeResultsToFile(filename, response):
    with open(filename, 'w') as outfile:
        json.dump(response, outfile)
    outfile.close()

if __name__ == "__main__":
    f = open(os.getenv("CUSTOMPATH") + "counter.txt", "r")
    counter = int(f.read())
    f.close()

    log = open(os.getenv("CUSTOMPATH") + "log.txt", "a")
    log.write("CRON started at: " + str(datetime.now()) + "\n")
    print ("is something happening??")

    
    # Wait.....
    rnd = random.randint(120,1500)
    #rnd = random.randint(3, 8)
    time.sleep(rnd)

    response = makeRequest()
    log.write("Made request at: " + str(datetime.now()) + "\n")
    
    # Add to master.csv
    sp = SplatoonResult.splatoonResult(response)
    if(sp.generateCSV()): # it actually DID something, save the file
        # Increase counter
        counter += 1
        # Write counter to file
        f = open(os.getenv("CUSTOMPATH") + "counter.txt", "w")
        f.write(str(counter))
        f.close()

        fn = os.getenv("CUSTOMPATH") + "archive/result" + str(counter) + ".json"
        # save to archive
        writeResultsToFile(fn, response)

        log.write("Recorded results at: " + fn + "\n")
    log.close()
        
        

    
