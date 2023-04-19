from .url_helper import extract_video_urls, url_to_dict, BASE_URL


def find_last_mime_request(video_url_dicts, mime_type='audio'):
    last_audio_request = None
    for d in video_url_dicts:
        if mime_type in d['mime'][0]:
            last_audio_request = d
    return last_audio_request


def generate_url(last_audio_request):
    base_url = last_audio_request[BASE_URL] + '?'
    last_audio_request.pop('range', None)
    last_audio_request.pop(BASE_URL, None)
    query_parameters = []

    for key, value in last_audio_request.items():
        query_parameters.append(f"{key}={value[0]}")

    new_url = base_url + "&".join(query_parameters)
    return new_url


def get_last_mime_url_by_entries(entries, mime_type='audio'):
    video_urls = extract_video_urls(entries)
    video_url_dicts = []
    for video_url in video_urls:
        video_url_dicts.append(url_to_dict(video_url))

    # 初始化最後一個音頻請求的變量
    last_audio_request = find_last_mime_request(video_url_dicts, mime_type)
    
    # 移除'range'字段
    new_url = generate_url(last_audio_request)
    return new_url
