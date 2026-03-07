"""
Milestone 2: Embedding Generation
Generates vector embeddings using Sentence Transformer
"""
from sentence_transformers import SentenceTransformer
import pandas as pd
import pickle
import os

def generate_embeddings(input_file='data/clean_kcc.csv',
                       output_file='models/kcc_embeddings.pkl',
                       model_name='all-MiniLM-L6-v2'):
    """
    Generate embeddings for Q&A pairs using Sentence Transformer
    """
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    
    print(f"Loading cleaned data from {input_file}")
    df = pd.read_csv(input_file)
    
    # Combine question and answer for better semantic representation
    texts = []
    for _, row in df.iterrows():
        text = f"Question: {row['Question']} Answer: {row['Answer']}"
        texts.append(text)
    
    print(f"Generating embeddings for {len(texts)} entries...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Save embeddings
    os.makedirs('models', exist_ok=True)
    with open(output_file, 'wb') as f:
        pickle.dump(embeddings, f)
    
    print(f"Saved embeddings to {output_file}")
    return embeddings

if __name__ == "__main__":
    generate_embeddings()
