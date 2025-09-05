from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List

def create_faiss_index(documents: List[str], embedding_model_name: str = "sentence-transformers/all-mpnet-base-v2"):
    """
    Create a FAISS index from a list of documents using HuggingFace embeddings.

    Args:
        documents (List[str]): List of text documents to index.
        embedding_model_name (str): Name of the HuggingFace model to use for embeddings.

    Returns:
        FAISS: A FAISS index containing the document embeddings.
    """
    # sentence-transformers/all-mpnet-base-v2
    # Initialize the HuggingFace embeddings model
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    
    # Create the FAISS index from the documents
    faiss_index = FAISS.from_texts(documents, embeddings)
    
    return faiss_index

def retrieve_similar_documents(faiss_index: FAISS, query: str, k: int = 4):
    """
    Retrieve similar documents from the FAISS index based on a query.

    Args:
        faiss_index (FAISS): The FAISS index to search.
        query (str): The query string to find similar documents for.
        k (int): The number of similar documents to retrieve.

    Returns:
        List[str]: A list of similar documents.
    """
    # Perform the similarity search
    similar_docs = faiss_index.similarity_search(query, k=k)
    # return [doc.page_content for doc in similar_docs]
    return similar_docs
    