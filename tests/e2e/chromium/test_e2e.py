import pytest
import dotenv
import requests
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from todo_app import app                  
from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope='module')
def app_with_temp_board(): 
    dotenv.load_dotenv(dotenv.find_dotenv('.env'), override=True)
    from todo_app.config.trello import TrelloConfig
    TrelloConfig.BOARD_ID = create_trello_board(TrelloConfig)
    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))    
    thread.daemon = True    
    thread.start()    
    yield application
    thread.join(1)
    delete_trello_board(TrelloConfig, TrelloConfig.BOARD_ID)

def create_trello_board(config):
    params = { 'key': config.KEY, 'token': config.TOKEN, 'name': 'e2e test board', 'defaultLists': 'false' }
    response = requests.post(url='https://api.trello.com/1/boards', params=params)
    return response.json()['id']

def delete_trello_board(config, board_id):
    params = { 'key': config.KEY, 'token': config.TOKEN }
    response = requests.delete(url=f'https://api.trello.com/1/boards/{board_id}', params=params)
    if response.status_code != 200:
        raise Exception(f'Attempting to delete e2e test board returned status code: {response.status_code}')

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox') # TODO: this is nasty, can we get rid of it?
    with webdriver.Chrome(executable_path='./bin/chromedriver', options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    text_box = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element_by_id('title'))
    text_box.send_keys('Test Todo')
    submit_button = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element_by_id('item_add_button'))
    submit_button.click()
    countdown_message = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element_by_id('countdown'))
    countdown_text = countdown_message.text
    assert countdown_text.startswith('You will be redirected to the index page in')
    time.sleep(5)
    cards = WebDriverWait(driver, timeout=5).until(lambda d: d.find_elements_by_class_name('card-body'))
    assert cards[0].text.startswith('Test Todo')
