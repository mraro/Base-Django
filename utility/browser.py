import os

from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'  # This case is form windows intel
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


# print( CHROMEDRIVER_PATH ) if something wrong, copy result and open in explorer

def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)  # can you find options in cmd with "chromedriver.exe --h" or in web

    if os.environ.get('SHOW_SELENIUM_WINDOW') == '0':
        chrome_options.add_argument('--headless')

    service = Service(str(CHROMEDRIVER_PATH))

    browser_chrome = webdriver.Chrome(service=service, options=chrome_options)
    return browser_chrome


if __name__ == '__main__':
    browser = make_chrome_browser()  # has --headless as arg
    browser.get('https://web.whatsapp.com/')
    # browser.get('https://web.whatsapp.com/')

    sleep(5)
    browser.quit()
