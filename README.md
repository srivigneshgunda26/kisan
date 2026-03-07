# Kisan Call Centre Query Assistant

An AI-Powered Agricultural Helpdesk using OpenRouter LLM and FAISS

## Overview
The Kisan Call Centre Query Assistant is an intelligent agricultural query resolution system built for rural support and information dissemination. It leverages AI capabilities including OpenRouter LLM and semantic vector search (FAISS) to answer farmers' queries.

## Features
- Offline mode using FAISS vector search
- Online mode with OpenRouter LLM (Llama 3.1)
- Semantic query understanding
- Agricultural domain expertise (crops, pests, diseases, schemes)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Setup
```bash
python setup.py
```

### 3. Start the Application
```bash
streamlit run app.py
```

The app will open at http://localhost:8501

## Configuration

The `.env` file is already configured with your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-or-v1-...
MODEL_NAME=meta-llama/llama-3.1-8b-instruct:free
```

## Project Structure
```
├── app.py                      # Streamlit UI
├── setup.py                    # Complete setup script
├── requirements.txt            # Python dependencies
├── .env                        # API configuration (configured)
│
├── scripts/
│   ├── preprocess_data.py      # Data cleaning
│   ├── generate_embeddings.py  # Embedding generation
│   └── create_faiss_index.py   # FAISS indexing
│
├── utils/
│   ├── query_handler.py        # Query processing
│   └── llm_client.py           # OpenRouter integration
│
├── data/
│   └── sample_raw_kcc.csv      # Sample dataset
│
└── models/                     # Generated after setup
    ├── kcc_embeddings.pkl
    ├── faiss_index.bin
    └── meta.pkl
```

## Sample Queries
- How to control aphids in mustard?
- What is the treatment for leaf spot in tomato?
- How to apply for PM Kisan Samman Nidhi scheme?
- What fertilizer is recommended during flowering in maize?

## Documentation
- `SETUP_GUIDE.md` - Detailed installation instructions
- `USAGE_GUIDE.md` - How to use the application
- `ARCHITECTURE.md` - Technical architecture details

## License
MIT License
