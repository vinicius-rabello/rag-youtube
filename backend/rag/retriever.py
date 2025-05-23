import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.documents import Document

# Essa classe é responsável por recuperar documentos relevantes com base em um índice FAISS e um modelo de incorporação.
class MetadataFAISSRetriever:
    def __init__(self, index, embedding_model, embedding_dim, chunks_with_embeddings):
        self.index = index
        self.embedding_model = embedding_model
        self.embedding_dim = embedding_dim
        self.chunks_with_embeddings = chunks_with_embeddings
    
    # O método retrieve busca os documentos mais relevantes com base na consulta e no papel do usuário.
    def retrieve(self, query):
        query_embedding = np.array(self.embedding_model.embed_query(query))
        distances, indices = self.index.search(query_embedding.reshape(1, self.embedding_dim), k=15)
        
        retrieved_chunks = []
        for i in indices[0]:
            if i < len(self.chunks_with_embeddings):
                retrieved_chunks.append(self.chunks_with_embeddings[i])
        
        return retrieved_chunks
    
    # O método score_documents classifica os documentos recuperados com base na similaridade do cosseno entre a consulta e os documentos.
    def score_documents(self, query, retrieved_chunks):
        query_embedding = np.array(self.embedding_model.embed_query(query)).reshape(1, -1)
        
        chunk_embeddings = []
        for doc in retrieved_chunks:
            chunk_embedding = np.array(doc['embedding'])
            chunk_embeddings.append(chunk_embedding)
        chunk_embeddings = np.array(chunk_embeddings)
        
        similarities = cosine_similarity(query_embedding, chunk_embeddings).flatten()
        scored_chunks = [(doc, similarity) for doc, similarity in zip(retrieved_chunks, similarities)]
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        top_docs = []
        for chunk, _ in scored_chunks:
            doc = Document(
                page_content=chunk['text'],
                metadata = {k: chunk[k] for k in ('start', 'end', 'id')}
            )
            top_docs.append(doc)
        return top_docs