#!/usr/bin/env python
# coding: utf-8

##########################################################################################################
#Library list
import os
import pyodbc
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
import mysql.connector

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#################################################################################################################################
# importing log to database class from the determined location
drive = Path(__file__).drive
logger_module = ''

today = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0)
dateStart = today - timedelta(days=5)

rangeDates = []
nextDate = dateStart
print('Creating Custom Range of Dates...')
while nextDate <= today:
    rangeDates.append(nextDate.strftime("%Y-%m-%d"))
    nextDate = nextDate + timedelta(days=1)
print('Done! Downloading all files!')

if os.name == 'nt':
    jsonCred =  "{}\\Users\\$USERNAME\\Desktop\\Python-Scripts\\Vivint\\Gsheets\\".format(drive)
else:
    jsonCred =  "{}$HOME/Desktop/Python-Scripts/Vivint/Gsheets/".format(drive)

jsonCred = os.path.expandvars(jsonCred)

class GSheetsWorker():
    def __init__(self,logger,spreadSheet,sheet):
        self.logger_module = logger
        global logger_module
        logger_module = logger
        self.spreadSheet = spreadSheet
        self.sheet = sheet

    def sheetUpdater(self, data):
        try:

            data['DAYS'] = pd.to_datetime(data['DAYS']).dt.strftime("%Y-%m-%d")
            data['SAVE_TIME'] = pd.to_datetime(data['SAVE_TIME'],format="%I:%M %p").dt.strftime("%H:%M:%S")
        
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            vals = data.values.tolist()
            # for val in vals:
            #     if isinstance(val[0], datetime.date):
            #         val[0] = val[0].strftime("%Y-%m-%d")

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))
            # * Running Update by cell function
            # logger_module.pyLogger('info',msg='Running Filter views update function')
            # print('')
            # print('Running Filter views update function')
            # self.filterviewsUpdate()
        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass
    
    def get_sec(self, time_str):
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)

    def cellUpdater(self,celldata):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Update by cell function')
            print('Parsing Data for Update by cell function')
            sheetdf = pd.DataFrame(self.sheet.get_all_values())
            mu = sheetdf[2].str.find("MU")
            muindex = mu.isin([0.0,0]).idxmax()
            sheetdf.columns = sheetdf.iloc[muindex]
            headers = sheetdf.iloc[muindex].values.tolist()
            colToUpdate = headers.index('Duration')+1
            cell_list = []

            logger_module.pyLogger('running',msg='Creating cell array to update')
            print('Creating cell array to update')
            for celldata in celldata.itertuples():
                cellrow = sheetdf.index[sheetdf['UID'] == celldata[1]].tolist()
                cellrow = cellrow[0]+1
                value = celldata[2]
                cellToUpdate = Cell(row=cellrow,col=colToUpdate,value=value)
                cell_list.append(cellToUpdate)

            logger_module.pyLogger('running',msg='Inserting the array values via the spreadsheet values update query')
            print('Inserting the array values via the spreadsheet values update query')
            self.sheet.update_cells(cell_list)
            logger_module.pyLogger('running',msg='Succesfully updated the values: {}'.format(len(cell_list)))
            print('Succesfully updated the values: {}'.format(len(cell_list)))

        except Exception as e:
            print('Error Executing the Update by Cell function. Error is ',e)
            self.logger_module.pyLogger('error',msg='Error Executing the Update by Cell function. Error is {}'.format(e))
            pass

    def sheetUpdaterAgentProductivity(self, dataQuery):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Agent State raw tracker')
            print('Parsing Data for Query Tracker with calls data')
            data = pd.read_sql_query(selectAgentProductivity.format(dateStart.strftime('%Y-%m-%d')),sqlcon)
            data['Date'] = pd.to_datetime(data['Date']).dt.strftime("%Y-%m-%d")
            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')
            dataFilter = data[~data["uid"].isin(dataQuery["uid"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass
            
    def sheetUpdaterCalls(self, dataQuery):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Agent State raw tracker')
            print('Parsing Data for Query Tracker with calls data')
            data = pd.read_sql_query(selectCalls.format(dateStart.strftime('%Y-%m-%d')),sqlcon)
            data['start_time'] = pd.to_datetime(data['start_time']).dt.strftime("%Y-%m-%d %H:%M:%S")
            data['Date'] = pd.to_datetime(data['Date']).dt.strftime("%Y-%m-%d")
            data['Interval'] = pd.to_datetime(data['Interval']).dt.strftime("%H:%M:%S")

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')
            dataFilter = data[~data["id"].isin(dataQuery["id"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass

    def sheetUpdaterAuxCodesRaw(self, dataQuery):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Agent State raw tracker')
            print('Parsing Data for Query Tracker with calls data')
            data = pd.read_sql_query(selectAuxCodesRaw.format(dateStart.strftime('%Y-%m-%d')),sqlcon)
            data['date'] = pd.to_datetime(data['date']).dt.strftime("%Y-%m-%d")
            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')
            dataFilter = data[~data["uid"].isin(dataQuery["uid"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass

    def sheetUpdaterAgentActivityRAW(self, dataQuery):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Agent State raw tracker')
            print('Parsing Data for Query Tracker with calls data')
            data = pd.read_sql_query(selectAgentActivityRAW.format(dateStart.strftime('%Y-%m-%d')),sqlcon)
            data['start_time'] = pd.to_datetime(data['start_time']).dt.strftime("%Y-%m-%d %H:%M:%S")
            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')
            dataFilter = data[~data["uid"].isin(dataQuery["uid"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass

    def sheetUpdaterLoginLogoutRAW(self, dataQuery):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Agent State raw tracker')
            print('Parsing Data for Query Tracker with calls data')
            data = pd.read_sql_query(selectLoginLogoutRAW.format(dateStart.strftime('%Y-%m-%d')),sqlcon)
            data['date'] = pd.to_datetime(data['date']).dt.strftime("%Y-%m-%d")
            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')
            dataFilter = data[~data["uid"].isin(dataQuery["uid"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass

    def sheetUpdaterCallsSummary(self, dataQuery):
        try:
            logger_module.pyLogger('info',msg='Parsing Data for Agent State raw tracker')
            print('Parsing Data for Query Tracker with calls data')
            data = pd.read_sql_query(selectCallsSummary.format(dateStart.strftime('%Y-%m-%d')),sqlcon)
            data['Date'] = pd.to_datetime(data['Date']).dt.strftime("%Y-%m-%d")
            # data['half_hour_interval'] = pd.to_datetime(data['half_hour_interval']).dt.strftime("%H:%M:%S")

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')

            agentList = data["callee_login_id"].tolist()
            actList = data["service_name"].tolist()
            teamList = data["scenario_name"].tolist()
            dates = data["Date"].tolist()
            intervals = data["half_hour_interval"].tolist()
            # datesList = [date.strftime("%Y-%m-%d %H:%M:%S") for date in dates]
            
            sep = " - "
            uidList = [agent + sep + str(activity) + sep + str(team) + sep + date + sep + interval  for agent,activity,team,date,interval in zip(agentList,actList,teamList,dates,intervals)] 

            uidDF = pd.DataFrame(uidList,columns=['uid'])
            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)
            data['uid'] = data['uid'].str.replace("None","")
            # data.to_csv("summary.csv")
            

            logger_module.pyLogger('running',msg='Creating dataframe filtered by not available values in the google sheets dataframe')
            dataFilter = data[~data["uid"].isin(dataQuery["key"])]
            
            # * Inserting the dataframe values via the spreadsheet values append query
            logger_module.pyLogger('running',msg='Inserting the dataframe values via the spreadsheet values append query')
            print('Inserting the dataframe values via the spreadsheet values append query')
            dataFilter = dataFilter.replace({np.nan: None})
            vals = dataFilter.values.tolist()

            self.spreadSheet.values_append(self.sheet.title, {'valueInputOption': 'USER_ENTERED'},{'values':vals})
            logger_module.pyLogger('running',msg='Succesfully inserted the values: {}'.format(len(vals)))
            print('Succesfully inserted the values: {}'.format(len(vals)))

        except Exception as e:
            print(e)
            self.logger_module.pyLogger('error',msg='Error Parsing Data. Error is {}'.format(e))
            pass