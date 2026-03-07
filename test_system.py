"""
Test script to verify the system is working correctly
"""
import os
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import streamlit
        import sentence_transformers
        import faiss
        import requests
        import pandas
        import numpy
        print("✓ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_data_files():
    """Test if data files exist"""
    print("\nTesting data files...")
    
    required_files = [
        'data/clean_kcc.csv',
        'data/kcc_qa_pairs.json',
        'models/kcc_embeddings.pkl',
        'models/faiss_index.bin',
        'models/meta.pkl'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} not found")
            missing.append(file)
    
    if missing:
        print("\nRun: python setup.py")
        return False
    
    return True

def test_query_handler():
    """Test query handler"""
    print("\nTesting query handler...")
    try:
        from utils.query_handler import QueryHandler
        handler = QueryHandler()
        
        # Test query
        results = handler.retrieve_top_k("How to control aphids?", k=3)
        
        if results:
            print(f"✓ Retrieved {len(results)} results")
            print(f"  Sample: {results[0]['question'][:50]}...")
            return True
        else:
            print("❌ No results retrieved")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llm_client():
    """Test LLM client configuration"""
    print("\nTesting LLM client...")
    
    if not os.path.exists('.env'):
        print("⚠️  .env file not found (optional for offline mode)")
        return True
    
    try:
        from utils.llm_client import GraniteLLMClient
        client = GraniteLLMClient()
        print("✓ LLM client initialized")
        print("  Note: Actual API calls not tested to avoid charges")
        return True
    except Exception as e:
        print(f"⚠️  LLM client error: {e}")
        print("  System will work in offline mode only")
        return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Kisan Call Centre Query Assistant - System Test")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Data Files", test_data_files),
        ("Query Handler", test_query_handler),
        ("LLM Client", test_llm_client)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(r for _, r in results)
    
    if all_passed:
        print("\n✓ All tests passed! System is ready.")
        print("\nRun the application: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
