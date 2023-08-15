from database.record import stop_recording, record_audio
from database.transcripting import transcription_file
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import threading
from twocaptcha import TwoCaptcha



API_KEY = os.getenv('API_KEY')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')


def process_google_meet_link(URL):
    """
    Фу-ия для перехода к встрече по ссылке,
    :param URL:
    :return:
    """
    service = Service(executable_path='/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/chromedriver')
    # options = webdriver.ChromeOptions()
    # options.add_argument("--use-fake-ui-for-media-stream")
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    driver = webdriver.Chrome(service=service, options=options)
    #URL = 'ссылка на встречу'
    driver.get("https://accounts.google.com/signin")

    # Вход в аккаунт Google
    email_elem = driver.find_element("xpath", "//input[@type='email']")
    email_elem.send_keys(EMAIL)
    email_elem.send_keys(Keys.RETURN)
    time.sleep(2)  # Добавлено для паузы

    # Получение изображения капчи
    captcha_image_element = driver.find_element('css selector', '#captchaimg')
    captcha_image_url = captcha_image_element.get_attribute('src')
    #print(captcha_image_url)
    time.sleep(5)

    # Получение решения капчи & Ввод решения капчи
    captcha_input_element = driver.find_element('xpath', '//*[@id="ca"]')
    captcha_input_element.send_keys(captcha_solution(captcha_image_url))
    time.sleep(10)
    #captcha_input_element.send_keys(str(123456))
    captcha_input_element.send_keys(Keys.RETURN)
    time.sleep(5)

    password_elem = driver.find_element("xpath", "//input[@type='password']")
    password_elem.send_keys(PASSWORD)
    password_elem.send_keys(Keys.RETURN)
    time.sleep(5)  # Добавлено для паузы

    # Переход к встрече Google Meet
    driver.get(URL)
    time.sleep(10)  # время для загрузки

    # Присоединение к встрече
    #join_button = driver.find_element("xpath", "//*[@id="'xDetDlgVideo'"]/div[2]/div/div[1]/span/a")
    join_button = driver.find_element("css selector", "#yDmH0d > c-wiz > div > div > div:nth-child(14) > div.crqnQb > div > div.gAGjv > div.vgJExf > div > div > div.d7iDfe.NONs6c > div.shTJQe > div.jtn8y > div.XCoPyb > div:nth-child(1) > button > span")

    join_button.click()
    time.sleep(10)

    # Создаем поток для записи аудио
    audio_thread = threading.Thread(target=record_audio)
    count_participants_thread = threading.Thread(target=finish_record(URL))#(target=finish_record, args=(URL,))
    transcription_thread = threading.Thread(target=transcription_file('out.wav'))#(target=transcription_file, args=('out.wav',))

    try:
        # Запускаем поток записи аудио
        audio_thread.start()
        count_participants_thread.start()

        transcription_thread.start()


    finally:
        # Ожидаем завершения потока
        audio_thread.join()
        count_participants_thread.join()
        transcription_thread.join()

    # Закрыть браузер после окончания встречи
    driver.quit()



def captcha_solution(path):
    solver = TwoCaptcha(API_KEY)

    try:
        result = solver.normal(path)

    except Exception as e:
        sys.exit(e)

    else:
        return str(result["code"])



def get_participants_count(driver, CSS_SELECTOR_PARTICIPANTS):
    """
    Фу-ия читает кол-во участников
    :param driver:
    :param CSS_SELECTOR_PARTICIPANTS:
    :return:
    """
    try:
        participants_element = driver.find_element('css selector',CSS_SELECTOR_PARTICIPANTS)# path_participants
        return int(participants_element.text)
    except Exception as e:
        print(f"Error getting participants count: {e}")
        return None

def finish_record(URL):
    """
    фу-ия рекурсивная останавливает запись при условии
    :param URL:
    :return:
    """
    global recording_flag
    service = Service(executable_path='/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    URL_MEETING = URL
    CSS_SELECTOR_PARTICIPANTS = '#ow3 > div.T4LgNb > div > div:nth-child(14) > div.crqnQb > div.fJsklc.nulMpf.Didmac.G03iKb > div > div > div.jsNRx > div > div:nth-child(2) > div > div > div'
    #path_participants = '//*[@id="ow3"]/div[1]/div/div[14]/div[3]/div[11]/div/div/div[3]/div/div[2]/div/div/div'
    driver.get(URL_MEETING)
    time.sleep(5)  # Дайте странице время для загрузки

    # Присоединение к встрече
    join_button = driver.find_element("xpath", "//*[@id="'xDetDlgVideo'"]/div[2]/div/div[1]/span/a")
    #join_button = driver.find_element("xpath", '//*[@id="xDetDlgVideo"]/div[2]/div/div[1]/span/a')
    join_button.click()


    previous_count = None
    #start_time = time.time()
    while True:
        count = get_participants_count(driver,CSS_SELECTOR_PARTICIPANTS)
        if count is not None:
            print(f"Кол-во участников: {count}")

            if count == 1:
                if previous_count == 1:
                    print("Кол-во участников было в течение минуты. закругляемся...")
                    stop_recording()
                    break
                else:
                    previous_count = 1
                    time.sleep(60)  # Проверка после 1 минуты.
                    continue
            else:
                previous_count = count  # обновляем предыдущее значение

        time.sleep(10)  # Регулярная проверка каждые 10 секунд.
