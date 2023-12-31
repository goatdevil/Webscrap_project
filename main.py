import requests
import json
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import googlemaps


def get_my_ip():
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        ip = data["ip"]
        return ip


def localisation_for_ip(IP_adress):
    url_api = 'http://apiip.net/api/check'
    access_key='************'
    reponse=requests.get(url_api+'?accessKey='+access_key+'&ip='+IP_adress)
    results=reponse.json()
    longitude=results['longitude']
    latitude=results['latitude']

    return latitude,longitude


def find_links(restaurant_name):
    driver = selenium.webdriver.Firefox()
    driver.get('https://www.google.com/')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#L2AGLb > div:nth-child(1)').click()
    driver.find_element(By.TAG_NAME, 'textarea').send_keys(restaurant_name)
    driver.find_element(By.CSS_SELECTOR, '.FPdoLc > center:nth-child(1) > input:nth-child(1)').click()
    time.sleep(1)
    links = driver.find_elements(By.CLASS_NAME, 'JV5xkf')
    link_delivery=None
    link_reservation=None
    for link in links:
            if link.find_element(By.TAG_NAME, 'b').text == 'Réservations':
                link_reservation = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
            elif link.find_element(By.TAG_NAME, 'b').text == 'Commander':
                link_delivery = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.close()
    return link_reservation, link_delivery


def find_link(restaurant_name):
    driver = selenium.webdriver.Firefox()
    driver.get('https://www.google.com/')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#L2AGLb > div:nth-child(1)').click()
    driver.find_element(By.TAG_NAME, 'textarea').send_keys(restaurant_name)
    driver.find_element(By.CSS_SELECTOR, '.FPdoLc > center:nth-child(1) > input:nth-child(1)').click()
    time.sleep(1)
    try:
        link = driver.find_element(By.CLASS_NAME, 'JV5xkf').find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        link=None
    driver.close()
    return link


def find_restaurants(latitude,longitude):
    gmaps = googlemaps.Client(key='***************')
    reverse_geocode_result = gmaps.reverse_geocode((latitude,longitude))
    places_result = gmaps.places_nearby(location=reverse_geocode_result[0]['geometry']['location'], radius=2000,
                                        type='restaurant')

    results = places_result['results']
    results=results[:5]
    tab_restaurant = []
    for restaurant in results:
        place_id = restaurant['place_id']
        url = 'https://maps.googleapis.com/maps/api/place/details/json?fields=name,delivery,reservable&place_id=' + str(place_id) + '&key=***************'
        result = requests.get(url).json()
        print(result)
        name = result['result']['name']
        result = result['result']
        try:
            if result['delivery'] == True and result['reservable'] == True:
                link_reservation, link_delivery = find_links(name)
            elif result['delivery'] == True:
                link_delivery = find_link()
                link_reservation = None
            elif result['reservable'] == True:
                link_reservation = find_link(name)
                link_delivery = None
            else:
                link_reservation = None
                link_delivery = None
            tab_restaurant.append([name, link_delivery, link_reservation])
            print(tab_restaurant)
        except:None


    return tab_restaurant

def main ():
    ip=get_my_ip()
    latitude,longitude=localisation_for_ip(ip)
    tab_restaurant=find_restaurants(latitude,longitude)
    print(tab_restaurant)


main()

