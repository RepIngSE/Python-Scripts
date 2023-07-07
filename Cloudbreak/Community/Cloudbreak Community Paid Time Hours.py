#!/usr/bin/env python
# coding: utf-8
##########################################################################################################
#Importaciones para el programa 
#Library list
import selenium
import zipfile
import getpass
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import dateutil.parser
import pandas as pd
import numpy as np
import unicodedata
import requests
import os
import shutil
import time
import re
import json
import sys
import pyotp
import gspread
import GsheetsWorker
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import datetime
from WebFunctions import clicker, rclicker, typer, finder, downloadBucket, downloadWait, enableHeadless, everyDownloadChrome
import pathlib
from pathlib import Path

import importlib.util
drive = Path(__file__).drive

#CHANGE JSON DIRECTORY HERE
if os.name == 'nt':
    jsonCred =  "{}\\Users\\$USERNAME\\Desktop\\Python-Scripts\\Cloudbreak\Community".format(drive)
else:
    jsonCred =  "{}$HOME/Desktop/Python-Scripts/Cloudbreak\Community".format(drive)

jsonCred = os.path.expandvars(jsonCred)
#################################################################################################################################
#Descargar archivo 
#### DOWNLOAD DIRECTORY
if os.name == 'nt':
    #Windows
    downloadDir = '\\Cloudbreak_data\\'
elif os.name == 'posix':
    #Ubuntu
    downloadDir = '/Cloudbreak_data/'

#Otorgar ruta de directorio o crearlo de no estar ahi 
#Absolute Directory
fileDir = os.path.dirname(os.path.abspath(__file__))
downloadDir = fileDir + downloadDir
if not os.path.exists(downloadDir):
    os.makedirs(downloadDir)

#################################################################################################################################
#Identificar sistema 
#CHECK System
if os.name == 'nt':
    opsys = 'Windows'
elif os.name == 'posix':
    opsys = 'Linux'
if opsys == 'Windows':
    #Windows
    attDir = '\\PaidTime\\'
elif opsys == 'Linux':    
    #Ubuntu
    attDir = '/PaidTime/'

# profileDir = "{}\\Users\\$USERNAME\\Desktop\\chromedriver\\chromedriver\\Driver\\CloudbreakDriver\\Profile\\".format(drive)
# profileDir = os.path.expandvars(profileDir)

#########################################################################################
### FUNCTIONS

#############################################################################
#DELETE ALL FILES IN THE DLOAD DIRECTORY

filelist = [ f for f in os.listdir(downloadDir)]
for f in filelist:
    os.remove(os.path.join(downloadDir, f))

#Conexión con selenium 
# SELENIUM DRIVER SETUP
chromedriver = os.path.expandvars("{}\\Users\\$USERNAME\\Downloads\\chromedriver\\chromedriver.exe".format(drive))
capabilities = { 'chromeOptions':  { 'useAutomationExtension': False}}
WINDOW_SIZE = "1000,800"
chrome_options = webdriver.ChromeOptions()
preferences = {
  "download.default_directory": attDir,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
}
# chrome_options.add_argument("user-data-dir={}".format(profileDir))
chrome_options = Options()
chrome_options.add_experimental_option("prefs", preferences)
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(chromedriver,desired_capabilities = capabilities)
# driver = webdriver.Chrome(ChromeDriverManager(log_level=100).install(),options=chrome_options)
#ChromeOptions = options
#wait = WebDriverWait(driver, 300)
#enableHeadless(driver,attDir)
#############################################################################
#Link reporte (5,2,3,1)
print('Starting CloudBreak Extraction')
sites = {
    'paidTime':'https://cloudbreak.communitywfm.com/CommunityWeb/UI/Adherence/AgentStateTransactionReportOptions.aspx?s=1&r=1&idmenu=108'
    }

chromedriver_path = r'C:\Users\sara.cruz02\Downloads\chromedriver_win32 (1)\chromedriver.exe'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 300)

#Credenciales cloudbreak
user = 'knoah.supervisor@martti.us'
password = 'Cloudbreak.23'

urlSF= 'https://cloudbreak.okta.com/login/login.htm?fromURI=%2Fapp%2Fcloudbreak_communityweb_1%2FexkillybdifpoflfI1t7%2Fsso%2Fsaml'
driver.get(urlSF)
driver.maximize_window()

element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="okta-signin-username"]')))
element.send_keys(user)
#username  = driver.find_element(By.XPATH, '//input[@id="okta-signin-username"]').send_keys(user)
passwd = driver.find_element(By.XPATH, '//input[@id="okta-signin-password"]').send_keys(password)
x = 'By.XPATH'
selector = '//input[@id="okta-signin-submit"]'
clicker(selector,x,wait,driver)

time.sleep(10)

#Define fecha de la cual es requerida el reporte 
fecha_actual = datetime.datetime.now().date()
startDate = fecha_actual - datetime.timedelta(days=0)
endDate = fecha_actual
paidTimeDict = {}

for url in sites:
    try:
        driver.get(sites[url])
        time.sleep(3)
        print("Historical Schedule Adherence Report",url)
        x = 'By.XPATH'
        time.sleep(5)
    
        if url == 'paidTime':
            
            selector = '//span[text()="Historical schedule adherence report"]'
            clicker(selector,x,wait,driver)

            #Formatea las fechas actuales 
            selector = '//input[contains(@name,"$dpFromDate$DateValue")]'
            typer(selector, x, startDate.strftime("%d/%m/%Y"), wait, driver)
            time.sleep(2)

            selector = '//span[text()="Historical schedule adherence report"]'
            clicker(selector,x,wait,driver)

            #Formatea las fechas finales actuales 
            selector = '//input[contains(@name,"$dpThruDate$DateValue")]'
            typer(selector, x, endDate.strftime("%d/%m/%Y"), wait, driver)
            time.sleep(2)

            #Selecciona Applies to activity
            selector = '//input[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_ActivitySelector_txtCurrentActivityValue"]'
            finder(selector, x, wait, driver)
            driver.find_element(By.XPATH, selector).click()
            selector_option = '//a[contains(text(), "Vendor Intouch CX")]'
            finder(selector_option, x, wait, driver)
            driver.find_element(By.XPATH, selector_option).click()

            # Seleccionar la opción "Vendor Intouch CX"
            #selector = '//option[text()="Vendor Intouch CX"]'
            #clicker(selector, x, wait, activity_dropdown)

            selector = '//span[text()="Historical schedule adherence report"]'
            clicker(selector,x,wait,driver)

            selector = '//input[@value="Regenerate report"]'#'//div[@tb-test-id="Individual Call Log"]'
            clicker(selector,x,wait,driver)
            time.sleep(30)

            # Espera un máximo de 10 segundos para que el elemento esté presente
            wait = WebDriverWait(driver, 10)

            # Espera hasta que el elemento esté presente en el DOM
            elemento_valor = wait.until(EC.presence_of_element_located((By.XPATH, '//td[@class="right"]/span[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_lblTotalTransCount"]')))

            # Obtén el valor del elemento
            valor = elemento_valor.text

            # Imprime el valor
            print(valor)

            driver.switch_to.default_content()
                
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(120)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
    
            html = driver.page_source
            
            soup = BeautifulSoup(html,"lxml")

            # Encuentra el enlace de descarga del informe
            download_link = soup.find("a", {"class": "logo"})["href"]







            # Descarga el informe como archivo de Excel
            response = requests.get(download_link, stream=True)
            file_path = attDir + "Informe.xlsx"  # Ruta de destino deseada
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print("Informe descargado exitosamente")

    except Exception as e:
        print(e)
        continue

def CloudbreakParser(sheet, filelist, sites, spreadsheetsSheets):
    # * Parsing all Downloaded Attachments to a dataframe
    spreadSheets = {
        'EOD UpHealth (cloudbreak)' : '1B0HfeH9nR8ZkxfPwzJ9n85bSR31DCFt9cxU35niyaGM'
    }
for spFile in filelist:
    try:
                        
        excel_file = os.path.join(downloadDir,spFile)

        if sheet == " DB2": 

            #Inicio de la hoja de cálculo 
            data = pd.read_excel(excel_file, sheet_name=sheet,header=1)

            #Limpieza de datos
            data = data.replace({np.nan: None})
            cols = [c for c in data.columns if 'Unnamed' not in c]
            data = data[cols]

            #Campo formateado
            data["date"] = pd.to_datetime(data["date"]).dt.strftime('%Y-%m-%d')

            #Campos calculados
            data['Year'] = pd.to_datetime(data["date"]).dt.strftime('%Y')
            data["Month"] = pd.to_datetime(data["date"]).dt.strftime('%m')
            data["Day"] = pd.to_datetime(data["date"]).dt.strftime('%d')
            data['Weeknum'] = pd.to_datetime(data["date"]).dt.isocalendar().week
            data['Weekday'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1
            data['Date'] = (pd.to_datetime(data["date"]).dt.dayofweek + 1) % 7 + 1

            current_date = datetime.datetime.now().date()

            #Uid 
            dateList = data['date'].to_list()
            for i, date in enumerate(dateList):
                comment = f"Comentario {i+1}"
                comment_with_date = f"{comment} - {date}"

            sep = " - "
            uidlist = [date + sep + str(agent).replace(".0","") for date,agent in zip(dateList,agentidList)]
            uidDF = pd.DataFrame(uidlist,columns=['uid'])
            data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True)],axis=1)

            data = data.replace({np.nan: None})
            data = data.replace({'': None})

    except Exception as e:
        print('Error parsing file: {} . Error is: {}'.format(e))
        pass

def gsheetsUploader(data,spsh,sh):
    try:
        print('Connecting to Google services accounts with secret key')
        gc = gspread.service_account(filename=os.path.join(jsonCred,'cli-globo-d728b37c0cf6.json'))

        print('Opening Vivint REPORT RAW Spreadsheet')
        spreadSheetQuery = gc.open_by_key(spsh)

        #funcion Agent Schedules 
        if sh == "Executive summary":
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
    except Exception as e:
        print('Error uploading data: {} . Error is: {}'.format(sheet,e))
        pass

if __name__ == '__main__':
    try:

        filelist = [ f for f in os.listdir(downloadDir)]

        workbookEOD = ["Executive summary"]   

        spreadsheetsSheets = {
        "Executive summary": "DB2"
        }

        for sheet in workbookEOD:
            CloudbreakParser(sheet,filelist,spreadsheetsSheets)

    except Exception as e:
        print('Error at main python Process: ',e)
    print("Finished Vivint WF Script !!!")
raise SystemExit
