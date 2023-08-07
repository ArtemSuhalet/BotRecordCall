import datetime
import subprocess
import warnings

import torch
#import torchvision

import wave
import contextlib

from pyannote.audio import Audio
from pyannote.core import Segment

import openai
import whisper

from sklearn.cluster import AgglomerativeClustering
import numpy as np

from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cpu"))

warnings.filterwarnings('ignore')

def transcription_file(path):
    """
    Функция для транскрипции файла в текст
    :param path:
    :return:
    """

    if path[-3:] != 'wav':
        subprocess.call(['ffmpeg', '-i', path, '2.wav', '-y'])
        path = '2.wav'
    model = whisper.load_model('base.en')

    option = whisper.DecodingOptions(fp16=False)
    result = model.transcribe(path)
    segments = result["segments"]

    with contextlib.closing(wave.open(path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    embeddings = np.zeros(shape=(len(segments), 192))

    for i, segment in enumerate(segments):
        audio = Audio()
        start = segment["start"]
        # Whisper overshoots the end timestamp in the last segment
        end = min(duration, segment["end"])
        clip = Segment(start, end)
        waveform, sample_rate = audio.crop(path, clip)
        embeddings[i] = embedding_model(waveform[None])

    embeddings = np.nan_to_num(embeddings)
    num_speakers = 1

    clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(segments)):
        segments[i]["speaker"] = 'SPEAKER' + str(labels[i] + 1)

    save_target = 'transcribe.txt'

    with open(save_target, 'w') as f:
        for index, segment in enumerate(result['segments']):
            f.write(str(index + 1) + '\n')
            f.write(str(datetime.timedelta(seconds=segment['start'])) + '-->' + str(
                datetime.timedelta(seconds=segment['end'])) + '\n')
            f.write(segment['text'].strip() + '\n')
            f.write('\n')
    return save_target


path = "/Users/mymacbook/Documents/12.mp3"
transcript = transcription_file(path)