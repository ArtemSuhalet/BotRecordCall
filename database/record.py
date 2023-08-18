from database.meet_process import *
import soundcard as sc
import soundfile as sf



OUTPUT_FILE_NAME = "out.wav"  # Имя файла.
SAMPLE_RATE = 48000  # [Гц]. Частота дискретизации.

# Глобальный флаг для управления записью
recording_flag = True

def record_audio():

    global recording_flag
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        while recording_flag:
            data = mic.record(numframes=SAMPLE_RATE)
            sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

# def record_audio():
#     global recording_flag
#     num_frames_to_record = int(20 * SAMPLE_RATE)  # Записать 20 секунд аудио
#
#     with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
#         data = mic.record(numframes=num_frames_to_record)
#         sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

def stop_recording():
    global recording_flag
    recording_flag = False


