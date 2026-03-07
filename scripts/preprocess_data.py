"""
Milestone 1: Data Preprocessing
Loads raw KCC CSV file, cleans and standardizes Q&A pairs
"""
import pandas as pd
import json
import os

def preprocess_kcc_data(input_file='data/questionsv4.csv', 
                        output_csv='data/clean_kcc.csv',
                        output_json='data/kcc_qa_pairs.json'):
    """
    Clean and standardize KCC Q&A data
    """
    print("Loading raw KCC data...")
    
    # Try to load the large dataset first
    try:
        df = pd.read_csv(input_file, encoding='utf-8', on_bad_lines='skip')
        print(f"✓ Loaded {input_file}")
    except FileNotFoundError:
        # Fallback to raw_kcc.csv if questionsv4.csv doesn't exist
        input_file = 'data/raw_kcc.csv'
        df = pd.read_csv(input_file, encoding='utf-8', on_bad_lines='skip')
        print(f"✓ Loaded {input_file}")
    
    print(f"Original data shape: {df.shape}")
    
    # Check if it's the questionsv4.csv format (questions, answers columns)
    if 'questions' in df.columns and 'answers' in df.columns:
        print("✓ Detected questionsv4.csv format")
        df['Question'] = df['questions'].str.strip()
        df['Answer'] = df['answers'].str.strip()
        # Add default metadata
        df['Category'] = 'General'
        df['Crop'] = 'General'
        df['QueryType'] = 'General'
    else:
        # Original format with QueryText and KccAns
        print("✓ Detected standard KCC format")
        df = df.dropna(subset=['QueryText', 'KccAns'])
        df['Question'] = df['QueryText'].str.strip()
        df['Answer'] = df['KccAns'].str.strip()
    
    # Clean data
    df = df.dropna(subset=['Question', 'Answer'])
    df = df.drop_duplicates(subset=['Question', 'Answer'])
    
    # Filter out very short or invalid entries
    df = df[df['Question'].str.len() > 10]
    df = df[df['Answer'].str.len() > 10]
    
    # Create clean dataset
    clean_df = df[['Question', 'Answer', 'Category', 'Crop', 'QueryType']].copy()
    
    print(f"Cleaned data shape: {clean_df.shape}")
    
    # Save as CSV
    os.makedirs('data', exist_ok=True)
    clean_df.to_csv(output_csv, index=False)
    print(f"Saved cleaned CSV to {output_csv}")
    
    # Save as JSON
    qa_pairs = []
    for _, row in clean_df.iterrows():
        qa_pairs.append({
            'question': row['Question'],
            'answer': row['Answer'],
            'category': row.get('Category', 'General'),
            'crop': row.get('Crop', 'General'),
            'query_type': row.get('QueryType', 'General')
        })
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(qa_pairs)} Q&A pairs to {output_json}")
    
    return clean_df

if __name__ == "__main__":
    preprocess_kcc_data()
