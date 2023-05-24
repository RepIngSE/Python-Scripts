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
import time
import os
#Retry function in case element is not clickable yet (Selector=buttoncode,x=by type IE By.XPATH)
def clicker(selector,x,wait,driver):

    while True:
        try:
            time.sleep(1)
            if x =='By.XPATH':
                wait.until(EC.element_to_be_clickable((By.XPATH, selector))).click()
            elif x == 'By.ID':
                wait.until(EC.element_to_be_clickable((By.ID, selector))).click()
                #driver.find_element_by_id(selector).click()
            elif x == 'By.CLASS_NAME':
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, selector))).click()
                #driver.find_element_by_class_name(selector).click()
            elif x == 'By.NAME':
                #wait.until(EC.element_to_be_clickable((, selector))).click()
                driver.find_element_by_name(selector).click()

        except Exception as e:
            print(str(e))
            print('Element not found or error in code, trying again in 5 secs...')
            time.sleep(5)
        else:
            break

#############################################################################################################
#Right Click Action, doesnt check if element exists! (Selector=buttoncode,x=by type IE By.XPATH)

def rclicker(selector,x,wait,driver):

    action = ActionChains(driver)
    while True:
        try:
            time.sleep(1)
            if x=='By.XPATH':
                action.move_to_element(driver.find_element(By.XPATH, selector)).perform()
                action.context_click().perform()
            elif x == 'By.ID':
                action.move_to_element(driver.find_element_by_id(selector)).perform()
                action.context_click().perform()
            elif x == 'By.CLASS_NAME':
                action.move_to_element(driver.find_element_by_class_name(selector)).perform()
                action.context_click().perform()
            elif x == 'By.NAME':
                action.move_to_element(driver.find_element_by_name(selector)).perform()
                action.context_click().perform()
            

        except Exception as e:
            print(str(e))
            print('Element not found or error in code, trying again in 5 secs...')
            time.sleep(5)
        else:
            break
#############################################################################################################
#Looks for the field and type data. f(Selector,by.element,text to type in textbox)

def typer(selector,x,y,wait,driver):

    while True:
        try:
            time.sleep(1)
            if x=='By.XPATH':
                wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            elif x == 'By.ID':
                wait.until(EC.element_to_be_clickable((By.ID, selector)))
            elif x == 'By.CLASS_NAME':
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, selector)))
            elif x == 'By.NAME':
                #wait.until(EC.element_to_be_clickable((, selector))).click()
                driver.find_element_by_name(selector)

        except Exception as e:
            print(str(e))
            print('Element not found or error in code, trying again in 5 secs...')
            time.sleep(5)

        else:
            if x=='By.XPATH':
                driver.find_element(By.XPATH, selector).clear()
                driver.find_element(By.XPATH, selector).send_keys(y)
            elif x == 'By.ID':
                driver.find_element_by_id(selector).clear()
                driver.find_element_by_id(selector).send_keys(y)
            elif x == 'By.CLASS_NAME':
                driver.find_element_by_class_name(selector).clear()
                driver.find_element_by_class_name(selector).send_keys(y)
            elif x == 'By.NAME':
                #wait.until(EC.element_to_be_clickable((, selector))).click()
                driver.find_element_by_name(selector).clear()
                driver.find_element_by_name(selector).send_keys(y)
            break

#############################################################################################################
#Finds a field finder finder(selector,by.element)
def finder(selector,x,wait,driver):

    while True:
        try:
            time.sleep(1)
            if x =='By.XPATH':
                wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            elif x == 'By.ID':
                wait.until(EC.element_to_be_clickable((By.ID, selector)))
            elif x == 'By.CLASS_NAME':
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, selector)))

        except Exception as e:
            print(str(e))
            print('Element not found or error in code, trying again in 5 secs...')
            time.sleep(5)
        else:
            break

#############################################################################################################
#Downloads checker dload_bucket(chromedriver variable)

def downloadBucket(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.file_url);
        """)
#############################################################################################################
#Checks for filename and if it was dowloaded, can be endswith or startwith download_wait(filename)

def downloadWait(filename,driver,wait,downloadDir):
    trigger= False
    while not trigger:
        for file in os.listdir(downloadDir):
            if file.endswith(filename):
                trigger= True
            else:
                print("file still not downloaded")
                time.sleep(5)

    wait.until(downloadBucket(driver))

#############################################################################################################
#HEADLESS CHROMEDRIVER DOWNLOAD FIX

def enableHeadless(browser,downloadDir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': downloadDir}}
    browser.execute("send_command", params)

def everyDownloadChrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
        #alert_obj = driver.switch_to.alert
        #alert_obj.accept()
    return driver.execute_script("""
    var items = downloads.Manager.get().items_
    if (items.every(e => e.state === "COMPLETE"))
        return items.map(e => e.file_url)
    """)