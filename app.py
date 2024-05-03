
import gradio as gr
import os,io

import soundfile as sf
import pyloudnorm as pyln


import subprocess
import json




def normalize_video_volume(video_file,loud):
    # 分析视频的平均音量
    # avg_volume = analyze_video_volume(video_file)

    # print(avg_volume)

    avg_volume = float(loud)

    # 使用EBU R128标准校正音频
    cmd = ['ffmpeg','-y','-i', video_file, '-af', f'loudnorm=I={avg_volume}:TP=-2:LRA=11','-c:v', 'copy', '-c:a', 'aac', "./output.aac"]

    subprocess.call(cmd)

    return "./output.aac"


def reference(input,top,loud):

    # 加载音频文件
    data, rate = sf.read(input)

    # 峰值归一化至 -1 dB
    peak_normalized_audio = pyln.normalize.peak(data, float(top))

    # 测量响度
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)

    # 响度归一化至 -12 dB LUFS
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, float(loud))

    sf.write("./normalized_audio.wav", loudness_normalized_audio, rate)

    return "./normalized_audio.wav"




def main():
    with gr.Blocks() as demo:
        gr.Markdown('# 音频响度统一 WebUI\n\n')
        with gr.Group():
            
            a_aud = gr.Audio(label="待处理音频", type="filepath")

            # top = gr.Textbox(label="峰值归一化",value="-1.0")

            loud = gr.Textbox(label="响度归一控制，LUFS的读数是负数，例如-5 LUFS，-10 LUFS，-13 LUFS等，数值越接近0，平均响度水平越高。",value="-5.0")

        
        btn = gr.Button('开始处理', variant='primary')

        aud = gr.Audio(label="处理结果",show_download_button=True)

        btn.click(normalize_video_volume, inputs=[a_aud,loud], outputs=[aud])


        gr.Markdown('WebUI by [刘悦的技术博客](https://space.bilibili.com/3031494).')


    demo.queue().launch(inbrowser=True,server_name="0.0.0.0",)

if __name__ == "__main__":
    main()
