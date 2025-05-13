from rag.youtube_parser import get_transcript, parse_transcript
from rag.embedder import generate_embeddings
from rag.prompt_builder import build_prompt_from_file
from rag.retriever import MetadataFAISSRetriever

from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
import faiss

import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def process_youtube_video(video_id):
    # Gets the transcript of a YouTube video and parses it into chunks
    transcript = get_transcript(video_id)
    chunks = parse_transcript(transcript, 60)

    # Generates embeddings for the chunks and creates a FAISS index
    embedding_vectors, chunks_with_embeddings = generate_embeddings(chunks, "text-embedding-3-small")
    embedding_dim = embedding_vectors[0].shape[0]

    # Creates a FAISS index for the embedding vectors
    index = faiss.IndexFlatL2(embedding_dim)

    # Adds the embedding vectors to the FAISS index
    index.add(embedding_vectors)

    # # Saves the FAISS index to a local file
    # faiss.write_index(index, "resources/index")

    return index, chunks_with_embeddings, embedding_dim

def process_query(query, index, chunks_with_embeddings, embedding_dim, model_name):
    # index = faiss.read_index("resources/index")
    embedding_model = OpenAIEmbeddings(model=model_name)

    retriever = MetadataFAISSRetriever(index, embedding_model, embedding_dim, chunks_with_embeddings)
    retrieved_docs = retriever.retrieve(query)
    most_relevant_docs = retriever.score_documents(query, retrieved_docs)
    prompt_template = build_prompt_from_file("resources/base_prompt.txt")
    llm = OpenAI(model="gpt-4.1-nano", temperature=0.1)
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    response = document_chain.invoke({"input": query, "context": most_relevant_docs})
    return response, most_relevant_docs