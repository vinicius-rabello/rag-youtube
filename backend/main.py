from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.utils import get_video_id_from_youtube_url
from backend.rag.pipeline import process_youtube_video
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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/videos/")
def process_video(video_url: UrlInput):
    url = video_url.url
    video_id = get_video_id_from_youtube_url(url)
    process_youtube_video(video_id)
    return {"message": f"Video with ID {video_id} processed successfully."}