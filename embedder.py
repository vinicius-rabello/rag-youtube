from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_embeddings(chunks, model_name):
    embedding_model=OpenAIEmbeddings(model=model_name, )
    embedding_vectors=[]
    for chunk in chunks:
        embedding = embedding_model.embed_query(chunk['text'])
        embedding_vectors.append(embedding)

    return np.array(embedding_vectors)
