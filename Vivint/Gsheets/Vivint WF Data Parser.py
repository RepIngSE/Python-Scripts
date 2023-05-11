#!/usr/bin/env python
# coding: utf-8
##########################################################################################################
#Library list
import imaplib
import email
import datetime as dt
from datetime import datetime,timedelta

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
        print('Error with email fuction: {}'.format(e))

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
                    

                        if sheet == "Agent Schedules":

                            ##Loading Dataframe for agent schedules
                            data = pd.read_excel(os.path.join(downloadDir,spFile), sheet_name=sheet,header=13)

                            ## Data Filtering or Mask for the lob
                            data = data[data["mu"]==lob]

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
                            'Duration'

                            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
                            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
                            data['Weekday'] = pd.to_datetime(data["date"]).dt.dayofweek
                            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')

                            data["Duration"] = pd.Timedelta(pd.to_datetime(data["activity_end"].astype(str)) - pd.to_datetime(data["activity_start"].astype(str))).seconds

                            ###
                            dateList = data['date'].to_list()
                            agentidList = data['agent_id'].to_list()

                            sep = " - "
                            uidlist = [date + sep + agent for date,agent in zip(dateList,agentidList)]
                            uidDF = pd.DataFrame(uidlist,columns=['uid'])
                            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

                            data = data.replace({np.nan: None})
                            data = data.replace({'': None})

                        vals = list(data.itertuples(index=False, name=None))
                        spreadsheet = spreadSheets[key]
                        if not vals:
                            print("Empty Dataframe...")
                        else:
                            gsheetsUploader(vals,spreadsheet,sheet)

                    except Exception as e:
                        print('Error parsing file: {} . Error is: {}'.format(f,e))
                        pass

        except Exception as e:
            print('Error parsing file: {} . Error is: {}'.format(f,e))
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
        }

        if sh == "Agent Schedules":
            sheet = spreadsheetsSheets[sh]
            try:
                print('Selecting {} '.format(sheet))
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(logger_module,spreadSheetQuery,sheetQuery)

                gsheetsWorker.sheetUpdaterAgentSchedules(data,dataQuery)
            

            except Exception as e:
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

            gsheetsWorker.sheetUpdaterCalls(dataQuery)
        elif "AgentProductivity" in sheet:
            gsheetsWorker.sheetUpdaterAgentProductivity(dataQuery)
        elif "AuxCodesRAW" in sheet:
            gsheetsWorker.sheetUpdaterAuxCodesRaw(dataQuery)
        elif "AgentActivityRAW" in sheet:
            gsheetsWorker.sheetUpdaterAgentActivityRAW(dataQuery)
        elif "LoginLogoutRAW" in sheet:
            gsheetsWorker.sheetUpdaterLoginLogoutRAW(dataQuery)
        elif "CallsSummary" in sheet:
            gsheetsWorker.sheetUpdaterCallsSummary(dataQuery)
        

    except Exception as e:
        print('Error with GS: {} . Error is: {}'.format(e))
        pass

if __name__ == '__main__':
    try:

        # email_downloader()

        filelist = [ f for f in os.listdir(downloadDir)]

        workbookEOD = ["Agent Schedules","Schedules","Adherence","Agent Activity","Occupancy"]
        
        lobs = {
            "Collections" : [
                "3100 Collections Tegucigalpa 24-7 InTouch Training"
               ,"3101 Collections Tegucigalpa 24-7 InTouch Nesting"  
               ,"3102 Collections Tegucigalpa 24-7 InTouch"              
            ]
            ,"Solutions" : [
                "1700 CS T1 Tegus Training"
               ,"1701 CS T1 Tegus Nesting"
               ,"1702 CS T1 Tegus"
               ,"1710 CS T2 Training"
               ,"1711 CS T2 Nesting"
               ,"1712 CS T2 Tegus"
               ,"1713 CS T2 Tegus Legancy"
               ,"1720 CS T3 Tegus training"
               ,"1721 CS T3 Tegus Nesting"
               ,"1722 CS T3 Tegus"
            ]
            ,"Retention" : [
                 "2400 CL EOT + ROR Tegucigalpa 24-7 InTouch Training"
                ,"2401 CL EOT + ROR Tegucigalpa 24-7 InTouch Nesting"
                ,"2402 CL EOT + ROR Tegucigalpa 24-7 InTouch"
            ]
            ,"Moves" : [
                 "2600 CL Moves Tegucigalpa 24-7 InTouch Training"
                ,"2601 CL Moves Tegucigalpa 24-7 Intouch Nesting"
                ,"2602 CL Moves Tegucigalpa 24-7 InTouch"
            ]
        }

        for sheet in workbookEOD:
            vivintEODParser(sheet,filelist,lobs)

    except Exception as e:
        print('Error at main python Process: ',e)
    print("Finished Vivint WF Script !!!")
raise SystemExit
