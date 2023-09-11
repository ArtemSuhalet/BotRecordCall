import wave

from selenium.common import NoSuchElementException

from database.record import setup_audio_stream, start_recording, save_audio_file, OUTPUT_FILENAME
from database.transcripting import transcription_file
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from twocaptcha import TwoCaptcha


API_KEY = os.getenv('API_KEY')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')


def captcha_solution(path):
    solver = TwoCaptcha(API_KEY)

    try:
        result = solver.normal(path)

    except Exception as e:
        sys.exit(e)

    else:
        return str(result["code"])


def setup_webdriver(EMAIL, PASSWORD, URL):
    service = Service(executable_path='/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/chromedriver')
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://accounts.google.com/signin")

    email_elem = driver.find_element("xpath", "//input[@type='email']")
    email_elem.send_keys(EMAIL)
    email_elem.send_keys(Keys.RETURN)
    time.sleep(2)

    password_elem = driver.find_element("xpath", "//input[@type='password']")
    password_elem.send_keys(PASSWORD)
    password_elem.send_keys(Keys.RETURN)
    time.sleep(5)

    driver.get(URL)
    WebDriverWait(driver, timeout=10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(10)
    driver.refresh()
    WebDriverWait(driver, timeout=15).until(lambda d: d.execute_script("return document.readyState") == "complete")
    join_button = driver.find_element("css selector",
                                      "#yDmH0d > c-wiz > div > div > div:nth-child(14) > div.crqnQb > div > div.gAGjv > div.vgJExf > div > div > div.d7iDfe.NONs6c > div.shTJQe > div.jtn8y > div.XCoPyb > div:nth-child(1) > button")
    join_button.click()
    return driver


def process_google_meet_link(URL, max_participants):
    # Ваши настройки исходной функции

    p, stream = setup_audio_stream()
    frames = []
    driver = setup_webdriver(EMAIL, PASSWORD, URL)
    time.sleep(10)

    # Запись аудио
    print('start record')
    start_recording(stream, frames, driver, URL)
    time.sleep(10)

    # Завершение записи и сохранение файла
    print('save file')
    save_audio_file(frames, p)
    time.sleep(10)

    # Транскрибирование файла
    print('start transcription')
    transcription_file(OUTPUT_FILENAME, max_participants)
    time.sleep(10)

    # Завершение работы с webdriver
    print('good riddance')
    driver.quit()


# #Получение изображения капчи
# captcha_elements = driver.find_elements('css selector', '#captchaimg')
# if captcha_elements:
#     captcha_image_element = captcha_elements[0]
#     captcha_image_url = captcha_image_element.get_attribute('src')
#     time.sleep(10)
#
#     captcha_input_element = driver.find_element('xpath', '//*[@id="ca"]')
#     captcha_input_element.send_keys(captcha_solution(captcha_image_url))
#     time.sleep(10)
#     captcha_input_element.send_keys(Keys.RETURN)
#     time.sleep(5)