"""
Complete setup script for Kisan Call Centre Query Assistant
Runs all preprocessing, embedding generation, and FAISS indexing steps
"""
import os
import sys

def run_setup():
    """
    Run complete setup pipeline
    """
    print("=" * 60)
    print("Kisan Call Centre Query Assistant - Setup")
    print("=" * 60)
    
    # Check if raw data exists
    if not os.path.exists('data/raw_kcc.csv'):
        print("\n⚠️  Warning: data/raw_kcc.csv not found!")
        print("Using sample data from data/sample_raw_kcc.csv")
        
        # Copy sample data
        import shutil
        os.makedirs('data', exist_ok=True)
        if os.path.exists('data/sample_raw_kcc.csv'):
            shutil.copy('data/sample_raw_kcc.csv', 'data/raw_kcc.csv')
            print("✓ Sample data copied to data/raw_kcc.csv")
        else:
            print("❌ Error: No data file found. Please add your KCC dataset to data/raw_kcc.csv")
            return False
    else:
        # If raw_kcc.csv exists, make sure it's properly formatted
        print("\n✓ Found data/raw_kcc.csv")
    
    # Step 1: Preprocess data
    print("\n" + "=" * 60)
    print("Step 1: Data Preprocessing")
    print("=" * 60)
    try:
        from scripts.preprocess_data import preprocess_kcc_data
        preprocess_kcc_data()
        print("✓ Data preprocessing completed")
    except Exception as e:
        print(f"❌ Error in preprocessing: {e}")
        return False
    
    # Step 2: Generate embeddings
    print("\n" + "=" * 60)
    print("Step 2: Generating Embeddings")
    print("=" * 60)
    try:
        from scripts.generate_embeddings import generate_embeddings
        generate_embeddings()
        print("✓ Embeddings generated successfully")
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return False
    
    # Step 3: Create FAISS index
    print("\n" + "=" * 60)
    print("Step 3: Creating FAISS Index")
    print("=" * 60)
    try:
        from scripts.create_faiss_index import create_faiss_index
        create_faiss_index()
        print("✓ FAISS index created successfully")
    except Exception as e:
        print(f"❌ Error creating FAISS index: {e}")
        return False
    
    # Setup complete
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Configure IBM Watsonx credentials in .env file")
    print("2. Run the application: streamlit run app.py")
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)
