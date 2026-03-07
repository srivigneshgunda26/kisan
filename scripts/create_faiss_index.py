"""
Milestone 2: FAISS Vector Store Creation
Creates FAISS index for fast similarity search
"""
import faiss
import pickle
import pandas as pd
import numpy as np
import os

def create_faiss_index(embeddings_file='models/kcc_embeddings.pkl',
                      data_file='data/clean_kcc.csv',
                      index_file='models/faiss_index.bin',
                      meta_file='models/meta.pkl'):
    """
    Create FAISS index from embeddings
    """
    print("Loading embeddings...")
    with open(embeddings_file, 'rb') as f:
        embeddings = pickle.load(f)
    
    print("Loading metadata...")
    df = pd.read_csv(data_file)
    
    # Prepare metadata
    metadata = []
    for _, row in df.iterrows():
        metadata.append({
            'question': row['Question'],
            'answer': row['Answer'],
            'category': row.get('Category', 'General'),
            'crop': row.get('Crop', 'General')
        })
    
    print(f"Creating FAISS index with {len(embeddings)} vectors...")
    dimension = embeddings.shape[1]
    
    # Create FAISS index (using L2 distance)
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    print(f"FAISS index created with {index.ntotal} vectors")
    
    # Save index
    os.makedirs('models', exist_ok=True)
    faiss.write_index(index, index_file)
    print(f"Saved FAISS index to {index_file}")
    
    # Save metadata
    with open(meta_file, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"Saved metadata to {meta_file}")
    
    return index, metadata

if __name__ == "__main__":
    create_faiss_index()
