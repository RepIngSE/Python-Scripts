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

if os.name == 'nt':
    userSpecs = importlib.util.spec_from_file_location("User.py", os.path.expandvars("{}\\Users\\$USERNAME\\Desktop\\Python-Scripts\\Vivint\\User.py".format(drive)))
else:
    userSpecs = importlib.util.spec_from_file_location("User.py", os.path.expandvars("{}$HOME/Desktop/Python-Scripts/Vivint/User.py".format(drive)))
userClass = importlib.util.module_from_spec(userSpecs)
userSpecs.loader.exec_module(userClass)

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
            if '.zip' in f:
                os.remove(os.path.join(downloadDir, f))
            else:
            shutil.rmtree(os.path.join(downloadDir, f))

        #############################################################################
        # * Get Email Attachments Code Block
        #Email User Data:
        email_user = 'sara.cruz02@24-7intouch.com'
        email_pass = 'Saragabriela2604*'
        host = 'imap.gmail.com'
        port= '993'

        # * Login to Email via IMAP with User an Pass specified. Selecting Inbox Folder where our emails at.
        print("Login to Email!!!")
        logger_module.pyLogger('info',msg='Login to email')
        mail = imaplib.IMAP4_SSL(host,port)
        mail.login(email_user, email_pass)
        mail.select('""')

        print("Searching mails...")
        logger_module.pyLogger('running',msg='Searching mails')
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
                                        logger_module.pyLogger('running',msg='Downloading: {}'.format(filename))    
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


### Workbook Pandas Parser
def vivintEODParser(sheet,filelist,lobs):
    # * Parsing all Downloaded Attachments to a dataframe
    spreadSheets = {
        'Collections' = ''
        ,'Solutions' = ''
    }
    for f in filelist:
        try:
            for key, val in tqdm(lobs.iteritems()):
                for lob in val:
                    print("Uploading Data for {}:".format(lob))

                    try:
                    
                        data = pd.read_excel(spFile, sheet_name=sheet)

                        if sheet = "Agent Schedules":

                            data = data[(data['team_name']=='24-7 Intouch New Hire') | (data['team_name']=='24-7 Intouch Guatemala')]

                            data = data.replace({np.nan: None})
                            cols = [c for c in data.columns if 'Unnamed' not in c]
                            data = data[cols]

                            data["start_time"] = data["start_time"].str.replace(' CST', '', regex=True)
                            data["start_time"] = data["start_time"].str.replace(' CDT', '', regex=True)

                            data["start_time"] = pd.to_datetime(data["start_time"],infer_datetime_format=True)


                        vals = list(data.itertuples(index=False, name=None))
                        spreadsheet = spreadSheets[key]
                        if not vals:
                            print("Empty Dataframe...")
                        else:
                            gsheetsUploader(vals,spreadsheet)

                    except Exception as e:
                        print('Error parsing file: {} . Error is: {}'.format(f,e))
                        pass

        except Exception as e:
            print(e)
            logger_module.pyLogger('critical',msg='Error parsing file: {} . Error is: {}'.format(f,e))
            pass

def gsheetsUploader(data,sh):
     try:
        logger_module.pyLogger('running',msg='Connecting to Google services accounts with secret key')
        print('Connecting to Google services accounts with secret key')
        gc = gspread.service_account(filename=os.path.join(jsonCred,'cli-globo-d728b37c0cf6.json'))

        print('Opening SunCountry REPORT RAW Spreadsheet')
        spreadSheetQuery = gc.open_by_key('1ePIqaEE3j4_Q9f-eWzCtfZY9F0s-jCFe909kvFcJk44')

        rawdataNICE = ["CallsSummary",'AgentProductivity','AuxCodesRAW','AgentActivityRAW','LoginLogoutRAW']

        for sheet in rawdataNICE:
            try:
                logger_module.pyLogger('running',msg='Selecting data sheet')
                print('Selecting {} '.format(sheet))
                
                logger_module.pyLogger('running',msg='Parsing selected sheet')
                # spreadSheetQuery.values_clear("{}!A2:U".format(sheet))
                sheetQuery = spreadSheetQuery.worksheet(sheet)
                dataQuery = pd.DataFrame(sheetQuery.get_all_values())
                dataQuery.columns = dataQuery.iloc[0]
                dataQuery = dataQuery.iloc[1:]
                dataQuery = dataQuery.reset_index()

                gsheetsWorker = GsheetsWorker.GSheetsWorker(logger_module,spreadSheetQuery,sheetQuery)

                print('Selecting parsing functions based on the report name')
                if sheet == "Calls":
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
                print('Error uploading data: {} . Error is: {}'.format(sheet,e))
                pass

    except Exception as e:
        print('Error with GS: {} . Error is: {}'.format(e))
        pass

if __name__ == '__main__':
    try:

        email_downloader()

        filelist = [ f for f in os.listdir(downloadDir)]

        workbookEOD = ["Agent Schedules","Schedules","Adherence","Agent Activity","Occupancy"]
        
        lobs = {
            "Collections" = [
                "3102 Collections Tegucigalpa 24-7 InTouch"
                ,"3101 Collections Tegucigalpa 24-7 InTouch Nesting"
                ,"3100 Collections Tegucigalpa 24-7 InTouch Training"            
            ]
            ,"Solutions" = [
                "1702 CS T1 Tegus"
            ]
        }

        for sheet in workbookEOD:
            vivintEODParser(sheet,filelist,lobs)

    except Exception as e:
        print('Error at main python Process: ',e)
    print("Finished SunCountry BP Script !!!")
raise SystemExit
