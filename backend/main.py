from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.utils import get_video_id_from_youtube_url
from backend.rag.pipeline import process_youtube_video, process_query
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlInput(BaseModel):
    url: str

class QueryInput(BaseModel):
    video_id: str
    query: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/videos/")
def process_video(video_url: UrlInput):
    url = video_url.url
    video_id = get_video_id_from_youtube_url(url)
    process_youtube_video(video_id)
    return {"message": f"Video with ID {video_id} processed successfully."}

@app.post("/query/")
def process_query_input(query: QueryInput):
    query_text = query.query
    video_id = query.video_id
    index, chunks, embedding_dim = process_youtube_video(video_id)
    response, relevant_chunks = process_query(
        query_text,
        index,
        chunks,
        embedding_dim,
        "text-embedding-3-small"
    )

    return {
        "response": response,
        "relevant_chunks": relevant_chunks
    }