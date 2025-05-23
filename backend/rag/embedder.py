from langchain_openai import OpenAIEmbeddings
import numpy as np
import os
from dotenv import load_dotenv

import sys
print(sys.executable)

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

load_dotenv(dotenv_path, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_embeddings(chunks, model_name):
    embedding_model=OpenAIEmbeddings(model=model_name, )
    embedding_vectors=[]
    chunks_with_embeddings=[]
    for chunk in chunks:
        embedding = embedding_model.embed_query(chunk['text'])
        embedding_vectors.append(embedding)
        chunk_with_embeddings = dict(chunk)
        chunk_with_embeddings['embedding'] = embedding
        chunks_with_embeddings.append(chunk_with_embeddings)

    return np.array(embedding_vectors), chunks_with_embeddings
