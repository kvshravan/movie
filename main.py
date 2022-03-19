from selenium import webdriver
from selenium.webdriver.common.by import By
import telegram_send
import time
import pexpect
import os

driver = None
prev = 0

def send_message():
    try:
        telegram_send.send(messages=['Tickets time :)'])
        print('Message sent')
    except Exception as e:
        print(e)
        print('Message failed')


def fetch_movie_tickets():
    global driver,prev
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    

    #browser.quit()
    while True:
        try:
            driver.get('https://in.bookmyshow.com/buytickets/rrr-hyderabad/movie-hyd-ET00094579-MT/')
            time.sleep(300)
            theatres_list = driver.find_element(By.ID,'venuelist')
            list_iter = theatres_list.find_elements(By.TAG_NAME,"li")
            if len(list_iter) > prev:
                send_message()
                prev = len(list_iter)
            else:
                print('No change')
        except Exception as e:
            print(e)
            print('No cinemas')
        time.sleep(300)    

if __name__ == '__main__':
    try:
        child = pexpect.spawn('telegram-send --configure')
        child.sendline('BOT_TOKEN')
        print(child.read())
    except Exception as e:
        print(e)
    fetch_movie_tickets()   
