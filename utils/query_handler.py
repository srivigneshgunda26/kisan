"""
Milestone 3: Semantic Query Pipeline
Handles query embedding and FAISS retrieval
"""
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

class QueryHandler:
    def __init__(self, 
                 model_name='all-MiniLM-L6-v2',
                 index_file='models/faiss_index.bin',
                 meta_file='models/meta.pkl'):
        """
        Initialize query handler with model and FAISS index
        """
        print("Loading Sentence Transformer model...")
        self.model = SentenceTransformer(model_name)
        
        print("Loading FAISS index...")
        self.index = faiss.read_index(index_file)
        
        print("Loading metadata...")
        with open(meta_file, 'rb') as f:
            self.metadata = pickle.load(f)
        
        print(f"Query handler initialized with {self.index.ntotal} entries")
    
    def retrieve_top_k(self, query, k=5):
        """
        Retrieve top-k most similar entries for a query
        """
        # Embed the query
        query_embedding = self.model.encode([query])
        
        # Search in FAISS
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Get results
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['distance'] = float(dist)
                results.append(result)
        
        return results
    
    def format_offline_answer(self, results):
        """
        Format retrieved results as offline answer
        """
        if not results:
            return "No relevant information found in the database."
        
        answer = "Based on Kisan Call Centre database:\n\n"
        
        # Get unique answers to avoid repetition
        seen_answers = set()
        count = 1
        
        for result in results:
            ans = result['answer']
            if ans not in seen_answers:
                answer += f"{count}. {ans}\n\n"
                seen_answers.add(ans)
                count += 1
                if count > 3:  # Limit to top 3 unique answers
                    break
        
        return answer.strip()
    
    def format_context_for_llm(self, results):
        """
        Format retrieved results as context for LLM
        """
        if not results:
            return ""
        
        context = "Relevant information from Kisan Call Centre database:\n\n"
        
        for i, result in enumerate(results[:3], 1):
            context += f"{i}. Q: {result['question']}\n"
            context += f"   A: {result['answer']}\n\n"
        
        return context
