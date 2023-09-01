
import time

import soundcard as sc
import soundfile as sf
import pyaudio
import wave
from selenium.common import NoSuchElementException

# Настройки записи
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
OUTPUT_FILENAME = "output.wav"

def setup_audio_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return p, stream

def start_recording(stream, frames, driver, URL):
    CSS_SELECTOR_PARTICIPANTS = '#ow3 > div.T4LgNb > div > div:nth-child(14) > div.crqnQb > div.fJsklc.nulMpf.Didmac.G03iKb > div > div > div.jsNRx > div > div:nth-child(2) > div > div > div'
    CSS_SELECTOR_END_RECORD_BUTTON = '#ow3 > div.T4LgNb > div > div:nth-child(14) > div.crqnQb > div.fJsklc.nulMpf.Didmac.G03iKb > div > div > div.Tmb7Fd > div > div.NHaLPe > span > button'

    previous_count = None
    while True:
        try:
            participants_element = driver.find_element('css selector', CSS_SELECTOR_PARTICIPANTS)
            count = int(participants_element.text)
            if count == 1:
                if previous_count == 1:
                    print("Количество участников было в течение минуты. Завершаем запись.")
                    # Нажимаем кнопку завершения записи
                    try:
                        end_record_button = driver.find_element('css selector', CSS_SELECTOR_END_RECORD_BUTTON)
                        end_record_button.click()
                    except NoSuchElementException:
                        print("Кнопка завершения записи не найдена.")
                    break
                else:
                    previous_count = 1
                    time.sleep(10)
                    continue
            else:
                previous_count = count
        except NoSuchElementException:
            print("Кнопка для подсчета участников не найдена. Завершаем запись.")
            break

        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    # Вариант проверки на изменение url после нажатия кнопки end
    # current_url = URL
    # while current_url == URL:
    #     data = stream.read(CHUNK, exception_on_overflow=False)
    #     frames.append(data)
    # else:
    #
    #     print("URL has changed, stopping audio recording")

def save_audio_file(frames, p):
    p.terminate()
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))




