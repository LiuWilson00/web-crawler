from urllib.parse import urlparse, parse_qs

BASE_URL = '___BASE_URL'

def extract_video_urls(entries):
    video_urls = []
    for entry in entries:
        url = entry["request"]["url"]
        if ".googlevideo.com/videoplayback" in url:
            video_urls.append(url)
    return video_urls


def url_to_dict(url):
    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)
    query_dict[BASE_URL] = url.split("?")[0]

    return query_dict