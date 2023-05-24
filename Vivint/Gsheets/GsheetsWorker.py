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
    jsonCred =  "{}\\Users\\$USERNAME\\Desktop\\Python-Scripts\\Vivint\\Gsheets\\".format(drive)
else:
    jsonCred =  "{}$HOME/Desktop/Python-Scripts/Vivint/Gsheets/".format(drive)

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

    #funcion AgentSchedules 
    def sheetUpdaterAgentSchedules(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','Duration','agent_id','agent_name','mu','date','shift_start','shift_end','scheduled_activity','activity_start','activity_end','uid']]

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

    # funcion Schedules 
    def sheetUpdaterSchedules(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','Date','Agent ID','Agent Name','Scheduled Activity','Length','Percent','TL','IF','T2','IF2','uid']]

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

    # funcion Adherence
    def sheetUpdaterAdherence(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','T Adh','Date','Agent ID','Agent Name','Scheduled Activities','Scheduled Time','Actual Time','Min. in Adherence','Min. out Adherence','Percent in Adherence','+/- Min. in Conformance','Percent in Conformance','Percent of Total Schedule','Percent of Total Actual','TL','uid']]

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

    # funcion Agent Activity
    def sheetUpdaterAgentActivity(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','Date','Agent ID','Agent Name','Agent Activity','Length','Percent','uid']]

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
    
    # funcion Agent Occupancy
    def sheetUpdaterOccupancy(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['N','Year','Month','Weeknum','Weekday','Day','OCC T','AHT T','Group','Entity ID','Entity Name','Day2','Date','Contacs handled','Outbound contacs','% Occ','Original hours req','Revised hours req', 'Provided hours sched', 'Provided hours estimated', 'Actual hours req', 'Combined AHT', 'Avg talk time', 'Avg work time', 'Avg out time', 'Total work vol CSS', 'uid' ]]

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