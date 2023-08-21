from selenium.common import NoSuchElementException

from database.record import record_audio
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
import requests
import threading
from twocaptcha import TwoCaptcha

import soundcard as sc
import soundfile as sf
#from handlers.default_handlers.echo import *

API_KEY = os.getenv('API_KEY')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')


def process_google_meet_link(URL, max_participants):
    """
    Фу-ия для перехода к встрече по ссылке,
    :param URL:
    :return:
    """
    try:
        service = Service(executable_path='/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/chromedriver')
        options = Options()
        options.add_argument("--use-fake-ui-for-media-stream")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://accounts.google.com/signin")

        # Вход в аккаунт Google
        email_elem = driver.find_element("xpath", "//input[@type='email']")
        email_elem.send_keys(EMAIL)
        email_elem.send_keys(Keys.RETURN)
        time.sleep(2)  # Добавлено для паузы


        #Получение изображения капчи
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

        password_elem = driver.find_element("xpath", "//input[@type='password']")
        password_elem.send_keys(PASSWORD)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(5)  # Добавлено для паузы

        # Переход к встрече Google Meet
        driver.get(URL)
        WebDriverWait(driver, timeout=10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(10)
        print('refresh page')
        driver.refresh()
        WebDriverWait(driver, timeout=15).until(lambda d: d.execute_script("return document.readyState") == "complete")
        join_button = driver.find_element("css selector",
                                          "#yDmH0d > c-wiz > div > div > div:nth-child(14) > div.crqnQb > div > div.gAGjv > div.vgJExf > div > div > div.d7iDfe.NONs6c > div.shTJQe > div.jtn8y > div.XCoPyb > div:nth-child(1) > button")
        join_button.click()
        time.sleep(15)


        # OUTPUT_FILE_NAME = "out.wav"  # Имя файла.
        # SAMPLE_RATE = 48000  # [Гц]. Частота дискретизации.
        # #global recording_flag
        # num_frames_to_record = int(10 * SAMPLE_RATE)  # Записать 20 секунд аудио
        #
        # with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(
        #         samplerate=SAMPLE_RATE) as mic:
        #     data = mic.record(numframes=SAMPLE_RATE)
        #     sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)
        # print('stop record')
        #
        # time.sleep(5)
        # Создаем поток для записи аудио
        # audio_thread = threading.Thread(target=record_audio)
        # #count_participants_thread = threading.Thread(target=finish_record(URL))#(target=finish_record, args=(URL,))
        # transcription_thread = threading.Thread(target=transcription_file, args=('/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/out.wav', max_participants))#(target=transcription_file, args=('out.wav',))

        try:
            recording_flag = True
            audio_thread = threading.Thread(target=record_audio, args=(recording_flag,))
            transcription_thread = threading.Thread(target=transcription_file, args=(
                '/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/out.wav', max_participants))

            # Запускаем поток записи аудио
            print(driver.current_url)
            print('start audio')
            audio_thread.start()

        #     while True:
        #         #if "meet.google.com" not in driver.current_url:
        #         if URL != driver.current_url:
        #             # Встреча закончилась, останавливаем запись и запускаем транскрипцию
        #             recording_flag = False  # Остановить запись аудио
        #             audio_thread.join()  # Дождаться завершения записи
        #             print('stop record')
        #
        #             # Запускаем поток для транскрипции
        #             print('start transcription')
        #             transcription_thread.start()
        #             transcription_thread.join()
        #             break
        #
        #         time.sleep(10)  # Подождать перед следующей проверкой
        # except Exception as e:
        #     print("An error occurred during the meeting:", str(e))
            # Пока кнопка по селектору не найдена на странице, ждем
            while True:
                try:
                    join_button = driver.find_element("css selector",
                                                      "#ow3 > div.T4LgNb > div > div:nth-child(14) > div.crqnQb > div.fJsklc.nulMpf.Didmac.G03iKb > div > div > div.Tmb7Fd > div > div.NHaLPe > span > button")
                    time.sleep(10)
                except NoSuchElementException:
                    # Кнопка не найдена, завершаем запись и начинаем транскрипцию
                    recording_flag = False
                    audio_thread.join()
                    print('stop record')

                    print('start transcription')
                    transcription_thread.start()
                    transcription_thread.join()
                    break
        except Exception as e:
            print("An error occurred during the meeting:", str(e))

        finally:
            # Закрыть браузер после окончания встречи

            driver.quit()
    except Exception as e:
        print("An error occurred:", str(e))

def wait_for_url_change(driver, initial_url):
    current_url = initial_url
    while current_url == driver.current_url:
        time.sleep(5)
    print('Meeting URL has changed. Meeting may have ended.')




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
    global max_participants
    service = Service(executable_path='/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    URL_MEETING = URL
    CSS_SELECTOR_PARTICIPANTS = '#ow3 > div.T4LgNb > div > div:nth-child(14) > div.crqnQb > div.fJsklc.nulMpf.Didmac.G03iKb > div > div > div.jsNRx > div > div:nth-child(2) > div > div > div'
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

            if count > max_participants:
                max_participants = count

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
