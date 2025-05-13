from rag.pipeline import process_youtube_video, process_query
from rag.response_parser import parse_response

video_id = input("Enter the YouTube video ID: ")
print("Processing video...")
index, chunks, embedding_dim = process_youtube_video(video_id, languages=["pt", "en"])
print("Video processed. You can now ask questions.")
while True:
    query = input("Enter your question (or 'exit' to quit)> ")
    if query.lower() == 'exit':
        break
    response, relevant_chunks = process_query(query, index, chunks, embedding_dim, "text-embedding-3-small")
    formatted_response = parse_response(response, relevant_chunks)
    print(formatted_response)