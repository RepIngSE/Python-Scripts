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
import json
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

            insert(self, data, dataQuery)


        except Exception as e:
            print(e)
            pass

    # funcion Schedules 
    def sheetUpdaterSchedules(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','date','agent_id','agent_name','scheduled_activity','Activity Duration','IF','T2','uid']]

            insert(self, data, dataQuery)

        except Exception as e:
            print(e)
            pass 

    # funcion Adherence
    def sheetUpdaterAdherence(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','T Adh','date','agent_id','agent_name','scheduled_activities','scheduled_time','actual_time','min_in_adherence','min_out_adherence','percent_in_adherence','min_in_conformance','percent_in_conformance','percent_of_total_schedule','percent_of_total_actual','uid']]
            
            insert(self, data, dataQuery)

        except Exception as e:
            print(e)
            pass 

    # funcion Agent Activity
    def sheetUpdaterAgentActivity(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','date','agent_id','agent_name','aux','duration','percent','uid']]

            insert(self, data, dataQuery)

        except Exception as e:
            print(e)
            pass 
    
    # funcion Agent Occupancy
    def sheetUpdaterOccupancy(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['N','Year','Month','Weeknum','Weekday','Day','OCC T','AHT T','entity_id','entity_name','day','date','contacts_handled','outbound_contacts','occ','original_hours_req','revised_hours_req', 'provided_hours_sched', 'provided_hours_estimated', 'actual_hours_req', 'combined_aht', 'avg_talk_time', 'avg_work_time', 'avg_out_time', 'total_work_vol_ccs', 'uid' ]]
            
            insert(self, data, dataQuery)
            
        except Exception as e:
            print(e)
            pass 
        
    # funcion Agent Details-AHT_Agent__Detail_T3
    def sheetUpdaterAgentDatails(self, data, dataQuery):
        try:
           
            print('Parsing Data for Query Tracker with calls data')
            data = data[['Year','Month','Weeknum','Weekday','Day','day','date','agent_id','agent_name','inbound_contacts','talk','work','total', 'att', 'awt', 'aht', 'outbound_contacts', 'outbound_time', 'system_time', 'uid' ]]
            
            insert(self, data, dataQuery)

        except Exception as e:
            print(e)
            pass 
    
    def delete_rows(self, indice_minimo, indice_maximo):
        if indice_maximo > indice_minimo: 
            self.sheet.delete_rows(indice_minimo, indice_maximo)

            print(indice_maximo-indice_minimo)
            
    #rango = "'{}'!A{}:{}{}".format(self.sheet.title, str(indice_minimo).replace(".0", ""), self.sheetcolumns, str(indice_maximo).replace(".0", ""))
    #self.spreadSheet.values_clear(rango)

def insert(self, data, dataQuery):

    # Insertar nuevas filas
    dataFilter = data[~data["uid"].isin(dataQuery["uid"])]

    print('Inserting the dataframe values via the spreadsheet values append query')
    dataFilter = dataFilter.replace({np.nan: None})
    vals = dataFilter.values.tolist()
    self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'}, {'values':vals})
    print('Successfully inserted the values: {}'.format(len(vals)))