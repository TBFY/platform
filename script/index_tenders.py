#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################################################################
# Harvester script for the TBFY Cross-lingual Search API (https://github.com/TBFY/search-API)
# 
# This file contains a script that load tender descriptions from TBFY data dump to the document repository.
# 
# Copyright: Universidad Politecnica de Madrid 2017-2020
# Author   : Carlos Badenes-Olmedo (cbadenes@fi.upm.es)
# License  : Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Project  : Developed as part of the TheyBuyForYou project (https://theybuyforyou.eu/)
# Funding  : TheyBuyForYou has received funding from the European Union's Horizon 2020
#            research and innovation programme under grant agreement No 780247
#####################################################################################################



import json
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
import os
import time
import glob
import sys, getopt, linecache, multiprocessing

START_TIME = default_timer()

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def fetch(session,file_url):
    if (not os.path.exists(file_url)):
        print(file_url, "not exists")
        return
    try:
        with open(file_url) as f:
          data = json.load(f)
          if ('releases' in data):
              for release in data['releases']:
                if ('tender' in release and 'ocid' in release):
                    ocid = release['ocid']
                    tender_data = release['tender']
                    document = {}
                    if ('description' in tender_data and 'id' in tender_data):
                        tender_id=tender_data['id']
                        id = ocid + "_" + tender_id
                        base_url = 'http://localhost:8080/search-api/documents/'
                        document['name']=tender_data['title']
                        if ('status' in tender_data):
                            document['tags']=tender_data['status']
                        text = tender_data['description']
                        if (len(text)>100):
                            document['text']=text
                            document['source']="tender"
                            document['date']=data['publishedDate'][0:12]+"00:00:00Z"
                            with session.post(base_url + id, json=document) as response:
                                print("{0:<30} {1:>20}".format(file_url, response.status_code))
                            
    except Exception as e:
        PrintException()
    

async def index_documents(directory,workers):
        
    print("From {0:<30} {1:>20}".format(directory, "Status"))
    START_TIME = default_timer()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        with requests.Session() as session:
                        
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, file) # Allows us to pass in multiple arguments to `fetch`
                )
                for file in glob.glob(directory+"/*.json")
            ]
            for response in await asyncio.gather(*tasks):
                pass
    elapsed = default_timer() - START_TIME
    time_completed_at = "{:5.2f}s".format(elapsed)
    print("Directory {0:<30} added at {1:>20}".format(directory, time_completed_at))

def main(argv):
    directories = []
    try:
      opts, args = getopt.getopt(argv,"hi",["idir="])
    except getopt.GetoptError:
      print('Usage: index-tenders.py -i <inputdirectory>')
      sys.exit(2)
    if (len(opts) == 0):
        print('Usage: index-tenders.py -i <inputdirectory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
         print('Usage: index-tenders.py -i <inputdirectory>')
         sys.exit()
        elif opt in ("-i", "--idir"):
         directories = args
      
    # Articles
    #directories = glob.glob(inputdir)
    
    #Parallel
    cpus = multiprocessing.cpu_count()
    workers = 2
    #if (cpus > 1):
    #    workers = cpus -1
    
    print("Max parallel workers:",workers)

    for directory in directories:
        if (os.path.isfile(directory)):
            continue
        
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(index_documents(directory,workers))
        loop.run_until_complete(future)
        
        
if __name__ == "__main__":
   main(sys.argv[1:])        
