# -*- coding:utf-8 -*-
import wave
import time
import datetime
import numpy as np
import pyaudio
from subprocess import Popen, PIPE


class Audio(object):

    def __init__(self):
        self.CHUNK = 8000  # 录音时每次采集的帧数
        self.FORMAT = pyaudio.paInt16  # 采样位数
        self.CHANNELS = 2  # 通道数
        self.RATE = 48000  # 采样率
        self.THRESHOLD = 3600  # 录音阈值

    def star_and_record(self, file_name):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        recording = False
        frames = []
        print("开始缓存录音")

        while (True):
            # 检测是否有声音
            if not recording:
                print('检测中... ')
                # 采集小段声音
                frames = []
                for i in range(0, 4):
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    frames.append(data)

                audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
                large_sample_count = np.sum(audio_data >= self.THRESHOLD / 3)

                # 如果有符合条件的声音，则开始录制
                # temp = np.max(audio_data)
                # if temp > THRESHOLD :
                if large_sample_count >= self.THRESHOLD * 1.8:
                    print("检测到信号")
                    recording = True
            else:
                while True:
                    print("持续录音中...")
                    subframes = []
                    for i in range(0, 5):
                        data = stream.read(self.CHUNK, exception_on_overflow=False)
                        subframes.append(data)
                        frames.append(data)

                    audio_data = np.frombuffer(b''.join(subframes), dtype=np.int16)
                    temp = np.max(audio_data)
                    if temp <= self.THRESHOLD * 0.8:
                        nowavenum += 1
                    else:
                        nowavenum = 0

                    if nowavenum >= 2:
                        print("等待超时，开始保存")

                        j = 1
                        while j > 0:
                            frames.pop()
                            j -= 1

                        # 保存声音文件
                        orignalWave = file_name
                        wf = wave.open(orignalWave, 'wb')
                        wf.setnchannels(self.CHANNELS)
                        wf.setsampwidth(p.get_sample_size(self.FORMAT))
                        wf.setframerate(self.RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()
                        stream.stop_stream()
                        stream.close()
                        p.terminate()
                        return file_name

    def play(self, file_name):
        # 只读方式打开wav文件
        wf = wave.open(file_name, 'rb')

        play = pyaudio.PyAudio()

        # 打开数据流
        stream = play.open(format=play.get_format_from_width(wf.getsampwidth()),
                           channels=wf.getnchannels(),
                           rate=wf.getframerate(),
                           output=True)

        # 读取数据
        data = wf.readframes(self.CHUNK)

        # 播放
        while data != b'':
            stream.write(data)
            data = wf.readframes(self.CHUNK)

        # 停止数据流
        stream.stop_stream()
        stream.close()

        # 关闭 PyAudio
        play.terminate()
        return


if __name__ == "__main__":
    audio = Audio()
    file_name = audio.star_and_record("aa.wav")
    time.sleep( 5 )
    audio.play(file_name)
