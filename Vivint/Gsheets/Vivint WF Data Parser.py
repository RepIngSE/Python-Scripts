#!/usr/bin/env python
# coding: utf-8
##########################################################################################################
#Library list
import imaplib
import email
import datetime as dt
from datetime import datetime,timedelta
import timeit
import cProfile
import pandas as pd
import numpy as np
import os
import datetime as dt
import shutil
import re

import pathlib
from pathlib import Path

import importlib.util
drive = Path(__file__).drive
from tqdm import tqdm

import GsheetsWorker
import gspread
import time

#################################################################################################################################
#Modules and DATABASE CONNECTOR

#CHANGE JSON DIRECTORY HERE
if os.name == 'nt':
    jsonCred =  "{}\\Users\\$USERNAME\\Desktop\\Python-Scripts\\Vivint\\Gsheets\\".format(drive)
else:
    jsonCred =  "{}$HOME/Desktop/Python-Scripts/Vivint/Gsheets/".format(drive)

jsonCred = os.path.expandvars(jsonCred)

#############################################################################################################
### FUNCTIONS

#### DOWNLOAD DIRECTORY
if os.name == 'nt':
    #Windows
    downloadDir = '\\VivintData\\'
elif os.name == 'posix':
    #Ubuntu
    downloadDir = '/VivintData/'

#Absolute Directory
fileDir = os.path.dirname(os.path.abspath(__file__))
downloadDir = fileDir + downloadDir
if not os.path.exists(downloadDir):
    os.makedirs(downloadDir)

#############################################################################
### FUNCTION PROCCESSES

### EMAIL DOWNLADER
def email_downloader():
    try:

        filelist = list(os.listdir(downloadDir))
        for f in filelist:
            os.remove(os.path.join(downloadDir, f))
            

        #############################################################################
        # * Get Email Attachments Code Block
        #Email User Data:
        email_user = 'sara.cruz02@24-7intouch.com'
        email_pass = 'ljphfkazgebxdskd'
        host = 'imap.gmail.com'
        port= '993'

        # * Login to Email via IMAP with User an Pass specified. Selecting Inbox Folder where our emails at.
        print("Login to Email!!!")
        mail = imaplib.IMAP4_SSL(host,port)
        mail.login(email_user, email_pass)
        mail.select('"Vivint EOD Data"')

        print("Searching mails...")
        now = datetime.now() - timedelta(days=1)
        #date handling de la función de email 
        today = datetime(now.year,now.month, now.day, 0, 0, 0) 
        today = today.strftime('%d-%b-%Y')
        searchcriteria = '(SENTSINCE "{}")'.format(today)

        # * Searching trough Inbox Folder with the Specified Criteria
        type, data = mail.search(None, searchcriteria)
        mails = data[0]
        mailIDs = mails.split()
        mailNo = 1

        try:
            # Cycling through email by email of the search result.
            for emailid in mailIDs:
                try:
                    resp, dataMail = mail.fetch(emailid, "(RFC822)")
                    emailBody = dataMail[0][1]
                    msg = email.message_from_bytes(emailBody)
                    # Checking MIME Encoding
                    if msg.is_multipart():
                        # Walking through email
                        for part in msg.walk():
                            try:
                                if part.get_content_maintype() == 'multipart':
                                    continue
                                if part.get('Content-Disposition') is None:
                                    continue
                                # getting Attachment and Download it at specified location
                                filename = str(mailNo) + " " + part.get_filename()
                                filename = filename.replace("\r\n","")
                                fileData = part.get_payload(decode=True)
                                # body = body.replace("\r"," ")
                                if filename is not None:
                                    savePath = os.path.join(downloadDir,filename)
                                    savePath = savePath.replace("24/7","")
                                    if not os.path.isfile(savePath):
                                        print("Downloading: ", filename)   
                                        fp = open(savePath, 'wb')
                                        fp.write(fileData)
                                        fp.close()
                                        mailNo = mailNo + 1
                            except Exception as e:
                                print('Error walking through email.Error is: {}'.format(e))
                                pass
                except Exception as e:
                    print('Error with email.Error is: {}'.format(e))
                    pass
            print("All Attachments Downloaded succesfully!!!")
        except Exception as e:
            print('Error with email extraction: {}'.format(e))
    except Exception as e:
        print('Error with email extraction:{}'.format(e))

### Workbook Pandas Parser
def vivintEODParser(sheet,filelist,lobs):
    # * Parsing all Downloaded Attachments to a dataframe
    spreadSheets = {
        'Collections' : '1q_BLGm27Ei45FnHJMc8ArVUwY_J8sUkTGvg8IxiwEBE'
        ,'Solutions' : '1G3JZXqkaPsCVjQCF0hp1BdRbNpuzNZ7awThYOxtUXrc'
        ,'Retention' : '1cVaffllFNcMOrnh8Y_IHPH3UnARl_5CDPsg_1tK9etg'
        ,'Moves' : '1o6DsJr3GplCojzReWLXa_p-N0CCIq9T3ufkWH7vm-wE'
    }
    for spFile in filelist:
        try:
            for key, val in tqdm(lobs.items()):
                for lob in val:
                    print("Uploading Data for {}:".format(lob))

                    try:
                        
                        excel_file = os.path.join(downloadDir,spFile)

                        if sheet == "Agent Schedules":

                            ##Loading Dataframe for agent schedules
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)

                            ## Data Filtering or Mask for the lob
                            data = data[data["mu"].isin(lob)]

                            ##Cleaning up the dataframe
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            ### Formatting DAtes for JSON upload to Gsheets
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')
                            data["shift_start"] = pd.to_datetime(data["shift_start"].astype(str)).dt.strftime('%H:%M:%S')
                            data["shift_end"] = pd.to_datetime(data["shift_end"].astype(str)).dt.strftime('%H:%M:%S')
                            data["activity_start"] = pd.to_datetime(data["activity_start"].astype(str)).dt.strftime('%H:%M:%S')
                            data["activity_end"] = pd.to_datetime(data["activity_end"].astype(str)).dt.strftime('%H:%M:%S')

                            ## Calculated Columns Handling

                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            data["Duration"] = ((pd.to_datetime(data["activity_end"].astype(str)) - pd.to_datetime(data["activity_start"].astype(str))).dt.total_seconds())/3600.0

                            ### Setting up UID for data
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                            #elif schedules 
                        elif sheet == "Schedules": 

                            #Inicio de la hoja de cálculo 
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)

                            #Filtro diccionario
                            data = data[data["mu"].isin(lob)]

                            #Limpieza de datos
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            #Campo formateado
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

                            #Campos calculados
                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1       
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            
                            #Campos calculados al final 
                            data['IF'] = data.apply(lambda row: 0 if row['scheduled_activity'] == "Lunch" else 1, axis=1)
                            data['T2'] = (pd.to_numeric(data["IF"]) * pd.to_numeric(data["Activity Duration"])*24); 

                            #Uid 
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                            #elif Adherence
                        elif sheet == "Adherence": 

                            #Inicio de la hoja de cálculo 
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)

                            #Filtro diccionario
                            data = data[data["mu"].isin(lob)]

                            #Limpieza de datos
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            #Campo formateado
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

                            #Campos calculados
                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            data['T Adh'] = pd.to_numeric(data["percent_in_adherence"])* pd.to_numeric(data ["scheduled_time"]); 
                            
                            #Uid 
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                            #elif Agent Activity 
                        elif sheet == "Agent Activity": 

                            #Inicio de la hoja de cálculo 
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)

                            #Filtro diccionario
                            data = data[data["mu"].isin(lob)]

                            #Limpieza de datos
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            #Campo formateado
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

                            #Campos calculados
                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            
                            #Uid 
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                            #elif occupancy
                        elif sheet == "Occupancy": 

                            #Inicio de la hoja de cálculo 
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)
                            
                            #Crear el mu, con entity id y entity name 
                            data['mu'] = data['entity_id'].astype(str) + " " + data['entity_name'] 

                            #Filtro diccionario
                            data = data[data["mu"].isin(lob)]

                            #Limpieza de datos
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            #Campo formateado
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

                            #Campos calculados
                            data['N'] = data.reset_index().index + 1
                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            data['OCC T'] = (pd.to_numeric(data["occ"])* pd.to_numeric(data ["provided_hours_estimated"]))/100; 
                            data['AHT T'] = pd.to_numeric(data["combined_aht"])* pd.to_numeric(data ["contacts_handled"]); 

                            #Uid 
                            dateList = data['date'].to_list()
                            agentidList = data['entity_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})
                        
                            #elif Agent datails - AHT_Agent_Detail_T3
                        elif sheet == "Agent Details": 

                            #Inicio de la hoja de cálculo 
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)

                            #Filtro diccionario
                            data = data[data["mu"].isin(lob)]

                            #Limpieza de datos
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            #Campo formateado
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

                            #Campos calculados
                            data['Tenure'] = np.where(data['AHT_Agent_Detail_T3'] < 2, "New Hires", "Tenure")
                            data['Months'] = ((datetime.today() + pd.DateOffset(days=1)) - data['AHT_Agent_Detail_T3'].dt.to_timestamp()) / np.timedelta64(30, 'D')
                            data['Months'] = np.ceil(data['Months']).fillna(0).astype(int)
                            data['Months'] = data['Months'].fillna(0)           
                            data['T AHT'] = data['Inbound Contacts'] * data['AHT'] * 8640
                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            
                            #Uid 
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                            #elif Agent datails - Calls per Agent T6 
                        elif sheet == "Agent Details": 

                            #Inicio de la hoja de cálculo 
                            data = pd.read_excel(excel_file, sheet_name=sheet,header=13)

                            #Filtro diccionario
                            data = data[data["mu"].isin(lob)]

                            #Limpieza de datos
                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            #Campo formateado
                            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

                            #Campos calculados
                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1
                            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
                            data['One'] =  pd.to_numeric(data["Count"])/ pd.to_numeric(data ["Count"]); 
                            data['Count'] =((data['agent_id'] == data['agent_id']) & (data['date'] == data['date'])).sum()
                            data['T TT'] = ((data['Talk'])*60*60*24)
                            data['T AWT'] =((data['AWT']*data['Inbound Contacs'])*86400)
                            data['T AHT'] =((['Inbound Contacs']*data['AHT']*data)*60*60*24)
                            
                            #Uid 
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                        vals = list(data.itertuples(index=False, name=None))
                        spreadsheet = spreadSheets[key]
                        if not vals:
                            print("Empty Dataframe...")
                        else:
                            gsheetsUploader(data,spreadsheet,sheet)

                    except Exception as e:
                        print('Error parsing file:. Error is: {}'.format(e))
                        pass

        except Exception as e:
            print('Error parsing file:. Error is: {}'.format(e))
            pass

def gsheetsUploader(data,spsh,sh):
    try:
        print('Connecting to Google services accounts with secret key')
        gc = gspread.service_account(filename=os.path.join(jsonCred,'cli-globo-d728b37c0cf6.json'))

        print('Opening Vivint REPORT RAW Spreadsheet')
        spreadSheetQuery = gc.open_by_key(spsh)

        spreadsheetsSheets = {
            "Agent Schedules": "New_Agent_schedules"
            ,"Schedules": "Time_Ut_Scheduled_(T1)"
            ,"Adherence": "Adherence_T5"
            ,"Agent Activity": "Time_Ut_Act(T2)"
            ,"Occupancy": "Occupancy T4"
            ,"Agent Details": ["AHT_Agent_Detail_T3","Calls per Agent T6"]
        }
        #funcion Agent Schedules 
        if sh == "Agent Schedules":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterAgentSchedules(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

        #funcion Schedules 
        elif sh == "Schedules":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterSchedules(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

        #funcion Adherence 
        elif sh == "Adherence":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterAdherence(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass
            
        #funcion Agent Activity 
        elif sh == "Agent Activity":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterAgentActivity(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass
        
        #funcion Occupancy 
        elif sh == "Occupancy":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterOccupancy(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

        #funcion Agent Details - AHT_Agent_Detail_T3 
        elif sh == "Agent Details":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterAgentDatailsAHT_Agent__Detail_T3(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

        #funcion Agent Details - AHT_Agent_Detail_T3 
        elif sh == "Agent Details":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                time.sleep(3)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterAgentDatails_Calls_per_Agent_T6(data,dataQuery)
        
            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

    except Exception as e:
        print('Error with GS: {} . Error is: {}'.format(e))
        pass

if __name__ == '__main__':
    try:

        email_downloader()

        filelist = [ f for f in os.listdir(downloadDir)]

        workbookEOD = ["Agent Schedules","Schedules","Adherence","Agent Activity","Occupancy","Agent Details"]

        lobs = {
            "Collections" : [[
                "3100 Collections Tegucigalpa 24-7 InTouch Training"
               ,"3100 Collections Tegucigalpa 24/7 InTouch Training"
               ,"3101 Collections Tegucigalpa 24-7 InTouch Nesting"  
               ,"3101 Collections Tegucigalpa 24/7 InTouch Nesting" 
               ,"3102 Collections Tegucigalpa 24-7 InTouch"  
               ,"3102 Collections Tegucigalpa 24/7 InTouch"            
            ]]
            ,"Solutions" : [[
                "1700 CS T1 Tegus Training"
               ,"1701 CS T1 Tegus Nesting"
               ,"1702 CS T1 Tegus"
               ,"1710 CS T2 Training"
               ,"1710 CS T2 Tegus Training"
               ,"1711 CS T2 Nesting"
               ,"1711 CS T2 Tegus Nesting"
               ,"1712 CS T2 Tegus"
               ,"1713 CS T2 Tegus Legacy"
               ,"1720 CS T3 Tegus training"
               ,"1720 CS T3 Tegus Training"
               ,"1721 CS T3 Tegus Nesting"
               ,"1722 CS T3 Tegus"
            ]]
            ,"Retention" : [[
                 "2400 CL EOT + ROR Tegucigalpa 24-7 InTouch Training"
                ,"2401 CL EOT + ROR Tegucigalpa 24-7 InTouch Nesting"
                ,"2402 CL EOT + ROR Tegucigalpa 24-7 InTouch"
                ,"2400 CL EOT + ROR Tegucigalpa 24/7 InTouch Training"
                ,"2401 CL EOT + ROR Tegucigalpa 24/7 InTouch Nesting"
                ,"2402 CL EOT + ROR Tegucigalpa 24/7 InTouch"
            ]]
            ,"Moves" : [[
                 "2600 CL Moves Tegucigalpa 24-7 InTouch Training"
                ,"2600 CL Moves Tegucigalpa 24/7 InTouch Training"
                ,"2601 CL Moves Tegucigalpa 24-7 Intouch Nesting"
                ,"2601 CL Moves Tegucigalpa 24/7 Intouch Nesting"
                ,"2602 CL Moves Tegucigalpa 24-7 InTouch"
                ,"2602 CL Moves Tegucigalpa 24/7 InTouch"
            ]]
        }

        for sheet in workbookEOD:
            vivintEODParser(sheet,filelist,lobs)

    except Exception as e:
        print('Error at main python Process: ',e)
    print("Finished Vivint WF Script !!!")
raise SystemExit
