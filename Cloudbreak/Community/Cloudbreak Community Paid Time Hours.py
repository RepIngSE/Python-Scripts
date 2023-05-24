#!/usr/bin/env python
# coding: utf-8
##########################################################################################################
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
import datetime as dt
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import dateutil.parser
import pandas as pd
import numpy as np
import unicodedata
import requests
import os
import shutil
import datetime as dt
import time
import re
import json
import sys
import pyotp

from WebFunctions import clicker, rclicker, typer, finder, downloadBucket, downloadWait, enableHeadless, everyDownloadChrome
import pathlib
from pathlib import Path

import importlib.util
drive = Path(__file__).drive

#################################################################################################################################
#MSSQL DATABASE CONNECTOR


#################################################################################################################################
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

#Absolute Directory
fileDir = os.path.dirname(os.path.abspath(__file__))
attDir = fileDir + attDir
if not os.path.exists(attDir):
    os.makedirs(attDir)

# profileDir = "{}\\Users\\$USERNAME\\Desktop\\chromedriver\\chromedriver\\Driver\\CloudbreakDriver\\Profile\\".format(drive)
# profileDir = os.path.expandvars(profileDir)

#########################################################################################
### FUNCTIONS

#############################################################################
#DELETE ALL FILES IN THE DLOAD DIRECTORY

filelist = [ f for f in os.listdir(attDir)]
for f in filelist:
    os.remove(os.path.join(attDir, f))

# SELENIUM DRIVER SETUP
chromedriver = os.path.expandvars("{}\\Users\\$USERNAME\\Desktop\\chromedriver\\chromedriver.exe".format(drive))
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
chrome_options.add_experimental_option("prefs",preferences )
chrome_options.add_argument("--disable-extensions")
chrome_options.set_capability("useAutomationExtension", False)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
#chrome_options.add_argument("--headless")
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
print('Starting CloudBreak Extraction')
sites = {
    'paidTime':'https://cloudbreak.communitywfm.com/CommunityWeb/UI/Adherence/AgentStateTransactionReportOptions.aspx?s=1&r=2&idmenu=115'
    }

driver = webdriver.Chrome(ChromeDriverManager(log_level=100).install(),options=chrome_options)
wait = WebDriverWait(driver, 300)

user = 'knoah.supervisor@martti.us'
password = 'Cloudbreak.23'

urlSF= 'https://cloudbreak.okta.com/login/login.htm?fromURI=%2Fapp%2Fcloudbreak_communityweb_1%2FexkillybdifpoflfI1t7%2Fsso%2Fsaml'
driver.get(urlSF)
driver.maximize_window()

username  = driver.find_element(By.XPATH, '//input[@id="okta-signin-username"]').send_keys(user)
passwd = driver.find_element(By.XPATH, '//input[@id="okta-signin-password"]').send_keys(password)
x = 'By.XPATH'
selector = '//input[@id="okta-signin-submit"]'
clicker(selector,x,wait,driver)

time.sleep(10)

endDate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0, 0)
startDate = endDate - timedelta(days=7)

paidTimeDict = {}

for url in sites:
    try:
        driver.get(sites[url])
        time.sleep(3)
        print("Browsing to the CloudBreak ",url)
        x = 'By.XPATH'
        time.sleep(5)
    
        if url == 'paidTime':
            
            selector = '//span[text()="Historical schedule adherence report"]'
            clicker(selector,x,wait,driver)

            selector = '//input[contains(@name,"$dpFromDate$DateValue")]'
            typer(selector,x,startDate.strftime("%m/%d/%Y"),wait,driver)
            time.sleep(2)

            selector = '//span[text()="Historical schedule adherence report"]'
            clicker(selector,x,wait,driver)

            selector = '//input[contains(@name,"$dpThruDate$DateValue")]'
            typer(selector,x,endDate.strftime("%m/%d/%Y"),wait,driver)
            time.sleep(2)

            selector = '//span[text()="Historical schedule adherence report"]'
            clicker(selector,x,wait,driver)

            selector = '//input[@value="Regenerate report"]'#'//div[@tb-test-id="Individual Call Log"]'
            clicker(selector,x,wait,driver)
            time.sleep(30)

            driver.switch_to.default_content()
                
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(120)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
    
            html = driver.page_source
            
            soup = BeautifulSoup(html,"lxml")

            agentStateTablesAgents = soup.find("table",{"id":"ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_AgentReportGrid"}).find('tbody').find_all('tr')
            for tables in agentStateTablesAgents:
                
                if tables.findChildren("span",{"class":"copyTitle4 wfmsg-fg-maroon"}): 
                    agent = tables.findChildren("span",{"class":"copyTitle4 wfmsg-fg-maroon"})
                    agent = agent[0].text

                if tables.findChildren("table",{"title":"Agent daily paid time"}): 
                    paidTable = tables.findChildren("table",{"title":"Agent daily paid time"})
                    agents = agent
                    agentName =  agents.split(" (")
                    agents = agentName[0]
                    key = agents
                    paidTimeDict[key] = paidTable[0]
                    tables.find_next("table",{"id":"ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_AgentReportGrid"})
               
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print("Succesfully Extracted the agent statetable data")
       
    except Exception as e:
        print(e)
        continue
driver.quit()
acum = 0
try:
    for agent in paidTimeDict:
        
        agentString = str(agent)
        agentName =  agentString.split("(")
        agentString = str(agentName[0]).strip()

        data = pd.read_html(str(paidTimeDict[agent]))
        data = data[0]
        data = data.replace({np.nan: None})
        cols = [c for c in data.columns if 'Unnamed' not in c]
        
        # data2 = data.drop(['Unnamed: 6','Unnamed: 11','Unnamed: 15'],axis=1)
        data = data[cols]
        data["agent"] = agentString
        data = data.replace(regex=['_'], value='')
        data["Schedule Date"] = pd.to_datetime(data["Schedule Date"],format="%A, %d %B %Y")
        data["Schedule Date"] = data["Schedule Date"].apply(lambda x: x.strftime("%Y-%m-%d"))

        scheduleDateList = data["Schedule Date"].tolist()

        dataDelete = data[["agent","Schedule Date"]]
        
        separator = " - "
        # aidListS = [aid + separator for aid in aidList]
        uidList = [i + separator + agentString for i in scheduleDateList] 

        uidDF = pd.DataFrame(uidList,columns=['uid'])
        data = pd.concat([data.reset_index(drop=True),uidDF.reset_index(drop=True),data.reset_index(drop=True)],axis=1)
        # data.to_csv("cloudbreak_community_paid_time.csv")
        vals = list(data.itertuples(index=False, name=None))
        delVals = list(dataDelete.itertuples(index=False, name=None))

        if not vals:
            print("Empty Dataframe...",agent)
        else:
            data.to_csv(agent + str(acum)+".csv")
            acum = acum +1
            print("Save this to a axcel or google sheets here")

except Exception as e:
    print(e)
print("Finished CloudBreak Tableau Script succesfully!!!")
raise SystemExit
