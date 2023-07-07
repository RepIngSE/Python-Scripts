#!/usr/bin/env python
# coding: utf-8

##########################################################################################################
#Library list
import os
import time
import pathlib
from pathlib import Path
import importlib
import importlib.util
import pandas as pd
import numpy as np
from gspread import Cell

import datetime
from datetime import datetime,timedelta

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#################################################################################################################################
# importing log to database class from the determined location
drive = Path(__file__).drive
logger_module = ''

if os.name == 'nt':
    jsonCred =  "{}\\Users\\$USERNAME\\Desktop\\Python-Scripts\\Cloudbreak\Community".format(drive)
else:
    jsonCred =  "{}$HOME/Desktop/Python-Scripts/Cloudbreak\Community".format(drive)

jsonCred = os.path.expandvars(jsonCred)

class GSheetsWorker():
    def __init__(self,spreadSheet,sheet):
        # global logger_module
        # logger_module = logger
        self.spreadSheet = spreadSheet
        self.sheet = sheet

    
    def get_sec(self, time_str):
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    def sheetUpdaterAgentDatails(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Day','Weeknum','Weekday','Date','Transaction Count','Scheduled In Queue','Actual In Queue','In Queue Variance','In Queue Variance %','Scheduled Out Of Queue','Actual Out Of Queue','Out Of Queue Variance','Out Queue Variance %','Total Scheduled','Total Variance','Total Adherence %','Non Scheduled / In Queue Hours']]

            dataFilter = data[~data["uid"].isin(dataQuery["uid"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            pass


        
