print('hello world')

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

import requests
import os
import io
from PIL import Image
import hashlib
import PIL

import random

from tkinter import Image
import selenium.webdriver as webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
DRIVER_PATH = 'C:/Users/olypa/.wdm/drivers/chromedriver/win32/98.0.4758.80/chromedriver.exe'
service = Service(DRIVER_PATH)
service.start()
wd = webdriver.Remote(service.service_url)
wd.quit()

count = 1

#----------------------------------------

n = 3 #number of images to get

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=3):
    def scroll_to_end(wd, scroll_point):  
        wd.execute_script(f"window.scrollTo(0, {scroll_point});")
        time.sleep(sleep_between_interactions)    
 
        
    # build the unsplash query
    search_url = f"https://unsplash.com/s/photos/{query}"
    # load the page
    wd.get(search_url)
    time.sleep(sleep_between_interactions)  
    
    image_urls = set()
    image_count = 0
    number_results = 0
    
    for i in range(1,2):
        scroll_to_end(wd, i*2)
        time.sleep(5)
        # thumb = wd.find_elements_by_css_selector("img._2zEKz")
        thumb = wd.find_elements_by_class_name('YVj9w')
        time.sleep(5)
        for img in thumb[0:n]:
            print(img)
            print(img.get_attribute('src'))
            image_urls.add(img.get_attribute('src'))
            image_count = len(image_urls)
            number_results = image_count
            time.sleep(.5)
        print(f"Found: {number_results} search results. Extracting links...")
        
    return image_urls

#-------------------------------------------------------------------------

def persist_image(folder_path:str,url:str,count):
    try:
        headers = {'User-agent': 'Chrome/64.0.3282.186'}
        image_content = requests.get(url, headers=headers).content
        
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = PIL.Image.open(image_file).convert('RGB')

        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

    new_name =  os.path.join(folder_path, "image" + str(count) + '.jpg')
    print(new_name)
    os.rename(file_path, new_name)


#------------------------------------------------------------------------

def search_and_download(search_term:str,driver_path:str, target_path='./images',number_images=3,count=1):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))


    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=3)
        for elem in res:
            persist_image(target_folder,elem,count)
            count += 1


search_terms = ['mug']
for search_term in search_terms:
    search_and_download(search_term=search_term, driver_path=DRIVER_PATH)





