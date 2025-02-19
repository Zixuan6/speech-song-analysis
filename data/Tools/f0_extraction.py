import librosa
import numpy as np
import datetime, csv
import os
import re

## This python script is used for extracting f0 and timepoint based on the pYIN algorithm. 
## This script can be used directly by setting input folder path and output folder path in line 54  & 55 

def get_f0(audiofilepath, output_folder):
    sr_target = 44100  # 目标采样率
    time_step = 0.005  # 每 0.005 秒采样一次 f0
    hop_length = int(sr_target * time_step)  # 计算 hop_length 确保间隔为 0.005s
   # N = 2048  # 计算 F0 时的帧长度
   # M = 512  # 计算 F0 时的步长
    #### 加载音频文件 ####
    y, sr = librosa.load(audiofilepath, mono=True)  # 加载音频文件，并转换为单声道
     #### 使用 pYIN 算法提取基频 (F0) ####
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, sr=sr, fmin=25, fmax=2048, frame_length=2048, hop_length=hop_length
    )
    t = librosa.times_like(f0, sr=sr, hop_length=hop_length)  # 计算时间轴对应的时间戳
    #### 处理缺失值 (NaN) ####
    f0[np.isnan(f0)] = 0  # 将 NaN 值替换为 0，避免计算时出错

    # 计算音频时长
    duration = librosa.get_duration(y=y, sr=sr)

    # 解析文件名，获取语言、日期、speaker、condition
    filename = os.path.basename(audiofilepath).replace('.wav', '')
    match = re.match(r"(\w+)_(\d+)_(s\d+)_(\w+)", filename)

    if match:
        language, date, speaker, condition = match.groups()
    else:
        language, date, speaker, condition = "conv", "sing"

    # 生成 CSV 输出文件路径
    filename = os.path.basename(audiofilepath).replace('.wav', '_f0.csv')
    outputfilepath = os.path.join(output_folder, filename)

    # 写入 CSV 文件
    with open(outputfilepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "f0", "language", "date", "speaker", "condition"])
        for i in range(len(t)):
            writer.writerow([t[i], f0[i], language, date, speaker, condition])

    print(f"✅ 处理完成: {filename} → {outputfilepath}")


if __name__ == "__main__":
    # 设置音频文件所在的文件夹和输出 CSV 的文件夹
    input_folder = "/Users/betty/Documents/MATLAB/song_speech_Mandarin/data/combined audio/"  # 替换成你的音频文件夹路径
    output_folder = "/Users/betty/Documents/MATLAB/song_speech_Mandarin/data/combined audio f0/"  # 替换成 CSV 输出路径

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历文件夹中的所有 .wav 文件
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

    # 逐个处理音频文件
    for wav_file in wav_files:
        audio_path = os.path.join(input_folder, wav_file)
        get_f0(audio_path, output_folder)

    print("🎉 所有音频文件处理完成！")
