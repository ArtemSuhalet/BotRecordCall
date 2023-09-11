import datetime
import subprocess
import warnings

import torch

import wave
import contextlib

from pyannote.audio import Audio
from pyannote.core import Segment


import whisper

from sklearn.cluster import AgglomerativeClustering
import numpy as np

from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cpu"))


warnings.filterwarnings('ignore')

def transcription_file(path, max_participants):
    """
    Функция для транскрипции файла в текст
    :param path:
    :return:
    """

    if path[-3:] != 'wav':
        subprocess.call(['ffmpeg', '-i', path, '22.wav', '-y'])
        path = '22.wav'
    model = whisper.load_model('tiny')

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
    num_speakers = max_participants


    clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(segments)):
        segments[i]["speaker"] = 'SPEAKER' + str(labels[i] + 1)

    save_target = 'transcribe1.txt'

    with open(save_target, 'w') as f:
        #for segment in result['segments']:
        for index, segment in enumerate(result['segments']):
            #f.write(str(index + 1) + '\n')
        #     f.write(str(datetime.timedelta(seconds=segment['start'])) + '-->' + str(
        #         datetime.timedelta(seconds=segment['end'])) + '\n')
            #f.write(segment['text'].strip() + '\n')
            f.write(str(index + 1) + '.' + segment['text'].strip())
            #f.write('\n')


