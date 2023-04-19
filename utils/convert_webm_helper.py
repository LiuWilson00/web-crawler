import os
import tempfile
import requests
from tqdm import tqdm
import hashlib
from moviepy.editor import *

def download_to_temp_folder(url):
    # 下載文件
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))

    # 創建暫存目錄和文件
    temp_folder = tempfile.mkdtemp()

    # 計算URL的哈希並將其添加到文件名中
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    temp_path = os.path.join(temp_folder, f'temp_{url_hash}.webm')

    # 將文件保存到暫存目錄
    with open(temp_path, 'wb') as f:
        for data in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit='KB'):
            f.write(data)

    return temp_path


def convert_mp4_and_delete_temp_file(temp_path, output_file,):
    
    # 確保 output 資料夾存在
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 讀取WebM文件並轉換為MP4
    video = VideoFileClip(temp_path)
    video.write_videofile(output_file, codec='libx264', audio_codec='aac')

    # 刪除原始WebM文件和暫存目錄
    os.remove(temp_path)
    os.rmdir(os.path.dirname(temp_path))


def convert_mp3_and_delete_temp_file(temp_path, output_file,):

    # 確保 output 資料夾存在
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 讀取WebM文件並轉換為MP4
    audio = AudioFileClip(temp_path)
    audio.write_audiofile(output_file, codec='mp3')

    # 刪除原始WebM文件和暫存目錄
    os.remove(temp_path)
    os.rmdir(os.path.dirname(temp_path))
