from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript = ytt_api.fetch(video_id, languages=['en'])
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def parse_transcript(transcript, max_window_duration):
    snippets = transcript.snippets
    chunks = []

    chunk = {
        "id": 0,
        "start": 0,
        "end": snippets[0].duration,
        "text": snippets[0].text
    }

    window_start = 0

    for i, snippet in enumerate(snippets[1:]):
        snippet_start = snippet.start
        snippet_duration = snippet.duration
        snippet_end = snippet_start + snippet_duration
        snippet_text = snippet.text

        if ((snippet_end - window_start) > max_window_duration) or (i == len(snippets) - 2):
            chunk["text"] = chunk["text"].replace("\xa0", " ").strip()
            chunks.append(chunk)
            chunk = {
                "id": f'chunk_{i+1}',
                "start": snippet_start,
                "end": snippet_end,
                "text": snippet_text
            }

            window_start = snippet_start
        else:
            chunk["end"] = snippet_end
            chunk["text"] += ' ' + snippet_text

    return chunks