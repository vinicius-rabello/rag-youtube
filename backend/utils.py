import time

def get_video_id_from_youtube_url(youtube_url):
    if "youtube.com/watch?v=" in youtube_url:
        return youtube_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_url:
        return youtube_url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL")
    
# Streamed response simulator
def response_streamer(response):
    response = response['response'] + "\nTimestamps: \n" + str(response['timestamps'])
    for word in response.split():
        yield word + " "
        time.sleep(0.02)