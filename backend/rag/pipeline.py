from backend.rag.youtube_parser import get_transcript, parse_transcript
from backend.rag.embedder import generate_embeddings
from backend.rag.prompt_builder import build_prompt_from_file
from backend.rag.retriever import MetadataFAISSRetriever

from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
import faiss

import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def process_youtube_video(video_id, languages=["en"]):
    if os.path.exists(f"backend/data/{video_id}_index.index") and os.path.exists(f"backend/data/{video_id}_chunks.json"):
        # Load the existing FAISS index and chunks
        index = faiss.read_index(f"backend/data/{video_id}_index.index")
        with open(f"backend/data/{video_id}_chunks.json", "r") as f:
            chunks_with_embeddings = json.load(f)
        embedding_dim = index.d

        return index, chunks_with_embeddings, embedding_dim
    # If the index and chunks do not exist, process the video
    # Gets the transcript of a YouTube video and parses it into chunks
    transcript = get_transcript(video_id, languages=languages)
    chunks = parse_transcript(transcript, 60)

    # Generates embeddings for the chunks and creates a FAISS index
    embedding_vectors, chunks_with_embeddings = generate_embeddings(chunks, "text-embedding-3-small")
    embedding_dim = embedding_vectors[0].shape[0]

    # Creates a FAISS index for the embedding vectors
    index = faiss.IndexFlatL2(embedding_dim)

    # Adds the embedding vectors to the FAISS index
    index.add(embedding_vectors)

    # Saves the FAISS index to a local file
    faiss.write_index(index, f"backend/data/{video_id}_index.index")

    with open(f"backend/data/{video_id}_chunks.json", "w", encoding='utf-8') as f:
        json.dump(chunks_with_embeddings, f, ensure_ascii=False)

    return index, chunks_with_embeddings, embedding_dim

def process_query(query, index, chunks_with_embeddings, embedding_dim, model_name):
    embedding_model = OpenAIEmbeddings(model=model_name)

    retriever = MetadataFAISSRetriever(index, embedding_model, embedding_dim, chunks_with_embeddings)
    retrieved_docs = retriever.retrieve(query)
    most_relevant_docs = retriever.score_documents(query, retrieved_docs)
    prompt_template = build_prompt_from_file("backend/resources/base_prompt.txt")
    llm = OpenAI(model="gpt-4.1-nano", temperature=0.1)
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    response = document_chain.invoke({"input": query, "context": most_relevant_docs})
    return response, most_relevant_docs