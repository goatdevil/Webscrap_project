import requests
import pandas as pd
import re
import json
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def test_restaurant_google(company_name):
    driver = selenium.webdriver.Firefox()
    driver.get('https://annuaire-entreprises.data.gouv.fr/')
    time.sleep(3)
    driver.find_element(By.ID, 'search-input-input').send_keys(company_name)
    driver.find_element(By.ID, 'search-input--lg').find_element(By.TAG_NAME, 'button').click()
    time.sleep(1)
    companies_list = driver.find_elements(By.CLASS_NAME, 'result-item')
    for companie in companies_list:
        test_name = companie.find_element(By.CSS_SELECTOR, 'a:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text
        if company_name.lower() == test_name.lower():
            driver.get(companie.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            time.sleep(1)
            APE_code = driver.find_element(By.CSS_SELECTOR,
                                           'div.jsx-1710981913:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > div:nth-child(1) > span:nth-child(1)').text
            if APE_code == '56.10A' or APE_code == '56.10C':
                driver.close()
                return True
            break
    driver.close()
    return False


def phone_search(company_name):
    driver = selenium.webdriver.Firefox()
    driver.get('https://www.google.com/')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#L2AGLb > div:nth-child(1)').click()
    driver.find_element(By.TAG_NAME, 'textarea').send_keys(company_name)
    driver.find_element(By.CSS_SELECTOR, '.FPdoLc > center:nth-child(1) > input:nth-child(1)').click()
    time.sleep(1)
    phonne_number = driver.find_element(By.CLASS_NAME, 'kno-fv').text
    time.sleep(1)
    driver.close()
    return str(phonne_number).replace(' ', '')


def call_API(phone_number):
    url_api = 'http://apilayer.net/api/validate'
    access_key = '85ea7fd026cd2073a765e3e5eef3ce2f'
    phone_number = phone_number[1:]
    print(phone_number)
    country_code = 'FR'
    format = '1'
    pattern = "?access_key=" + access_key + "&number=" + phone_number + "&country_code=" + country_code + "&format=" + format
    response = requests.post(url_api + pattern)
    return response.json()


def localisation_for_ip(IP_adress):
    url_api = 'https://apiip.net/api/check'
    access_key='4dd0ce6b-5aa9-45b8-a2ea-2f993df54943'
    reponse=requests.get(url_api+'?accessKey='+access_key+'&'+IP_adress)
    return reponse.json()

def find_near_restaurant(latitude,longitude):
    driver=selenium.webdriver.Firefox()
    driver.get('https://www.google.fr/maps')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,'.VtwTSb > form:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)').click()
    time.sleep(1)
    driver.find_element(By.ID,'searchboxinput').send_keys(latitude+','+longitude)
    driver.find_element(By.ID,'searchbox-searchbutton').click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,'div.KNfEk:nth-child(1) > button:nth-child(1)').click()
    time.sleep(3)
    list_name=driver.find_elements(By.CLASS_NAME,'NrDZNb')
    print(len(list_name))
    for name in list_name:
        print(name.text)

    restaurant_list=driver.find_element(By.CSS_SELECTOR,".w6Uhzf > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)").find_elements(By.XPATH,'./div')

    # for restaurant in restaurant_list:
    #     try:
    #         print(restaurant.find_element(By.CLASS_NAME,'NrDZNb').text)
    #         #print(restaurant.find_element(By.CSS_SELECTOR,'div:nth-child(5) > div:nth-child(1) > div:nth-child(3) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)').text)
    #     except:
    #         restaurant_list.remove(restaurant)




# company_name=input("nom d'un restaurant")
# company_name = "BUONA PIZZA (BUONA PIZZA)"
# if test_restaurant_google(company_name) == True:
#     phone_number = phone_search(company_name)
#     print(phone_number)
#     call_API(phone_number)
find_near_restaurant('48.814396','2.413131')