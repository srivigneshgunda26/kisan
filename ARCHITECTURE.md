# Kisan Call Centre Query Assistant - Architecture Documentation

## System Overview

The Kisan Call Centre Query Assistant is a hybrid AI system that combines:
- **Offline retrieval**: FAISS vector search for fast, reliable answers
- **Online generation**: IBM Watsonx Granite LLM for enhanced responses

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Query Handler                             │
│  - Embeds user query                                         │
│  - Retrieves top-k similar entries from FAISS                │
│  - Formats results for display and LLM                       │
└────────┬────────────────────────────────────────┬───────────┘
         │                                        │
         ▼                                        ▼
┌──────────────────┐                    ┌──────────────────┐
│  FAISS Index     │                    │  Granite LLM     │
│  - Vector search │                    │  - Context aware │
│  - Fast retrieval│                    │  - Natural lang  │
└──────────────────┘                    └──────────────────┘
         │                                        │
         ▼                                        ▼
┌──────────────────┐                    ┌──────────────────┐
│  Offline Answer  │                    │  Online Answer   │
│  (Retrieved Q&A) │                    │  (LLM Generated) │
└──────────────────┘                    └──────────────────┘
```

## Component Details

### 1. Data Preprocessing (Milestone 1)

**File**: `scripts/preprocess_data.py`

**Purpose**: Clean and standardize raw KCC data

**Process**:
1. Load raw CSV file
2. Remove duplicates and null values
3. Standardize column names
4. Filter invalid entries
5. Export to CSV and JSON formats

**Input**: `data/raw_kcc.csv`
**Output**: 
- `data/clean_kcc.csv`
- `data/kcc_qa_pairs.json`

### 2. Embedding Generation (Milestone 2)

**File**: `scripts/generate_embeddings.py`

**Purpose**: Convert text to dense vector representations

**Model**: `all-MiniLM-L6-v2` (Sentence Transformer)
- Dimension: 384
- Fast inference
- Good semantic understanding

**Process**:
1. Load cleaned data
2. Combine question + answer for each entry
3. Generate embeddings using Sentence Transformer
4. Save embeddings as pickle file

**Output**: `models/kcc_embeddings.pkl`

### 3. FAISS Index Creation (Milestone 2)

**File**: `scripts/create_faiss_index.py`

**Purpose**: Create searchable vector index

**Index Type**: IndexFlatL2 (exact search)
- Uses L2 (Euclidean) distance
- Exact nearest neighbor search
- No compression

**Process**:
1. Load embeddings
2. Create FAISS index
3. Add vectors to index
4. Save index and metadata

**Output**: 
- `models/faiss_index.bin`
- `models/meta.pkl`

### 4. Query Handler (Milestone 3)

**File**: `utils/query_handler.py`

**Purpose**: Process user queries and retrieve relevant information

**Key Methods**:

```python
retrieve_top_k(query, k=5)
# Embeds query and searches FAISS index
# Returns top-k most similar entries

format_offline_answer(results)
# Formats retrieved results for display
# Removes duplicates, limits to top 3

format_context_for_llm(results)
# Prepares context for LLM prompt
# Includes Q&A pairs from database
```

**Flow**:
1. User query → Embed using Sentence Transformer
2. Search FAISS index for similar vectors
3. Retrieve metadata for top-k results
4. Format for offline display and LLM context

### 5. LLM Client (Milestone 4)

**File**: `utils/llm_client.py`

**Purpose**: Interface with IBM Watsonx Granite LLM

**Model**: `ibm/granite-3-8b-instruct`
- 8B parameters
- Instruction-tuned
- Hosted in Frankfurt region

**Authentication**:
- Uses IBM Cloud IAM
- API key → Access token
- Token included in requests

**Parameters**:
- `max_new_tokens`: 500
- `temperature`: 0.7
- `top_p`: 0.9
- `repetition_penalty`: 1.1

**Prompt Structure**:
```
You are an agricultural expert assistant...

Context:
[Retrieved Q&A from FAISS]

Farmer's Question: [User query]

Answer:
```

### 6. Streamlit UI (Milestone 5)

**File**: `app.py`

**Purpose**: User-facing web interface

**Features**:
- Query input with sample queries
- Dual-mode display (offline + online)
- Loading indicators
- Error handling
- Responsive design

**Layout**:
- Sidebar: Info, sample queries, settings
- Main area: Query input, search button
- Results: Two-column layout (offline | online)
- Expandable sections for detailed results

## Data Flow

### Query Processing Flow

```
1. User enters query
   ↓
2. Query Handler embeds query
   ↓
3. FAISS searches for similar vectors
   ↓
4. Top-k results retrieved
   ↓
5a. Format as offline answer → Display
   ↓
5b. Format as context for LLM
   ↓
6. LLM generates enhanced answer
   ↓
7. Display online answer
```

### Setup Flow

```
1. Raw data (CSV)
   ↓
2. Preprocessing → Clean data
   ↓
3. Embedding generation → Vectors
   ↓
4. FAISS indexing → Searchable index
   ↓
5. Ready for queries
```

## Technology Stack

### Core Libraries
- **Streamlit**: Web UI framework
- **Sentence Transformers**: Text embedding
- **FAISS**: Vector similarity search
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

### AI/ML Components
- **Sentence Transformer Model**: all-MiniLM-L6-v2
- **IBM Watsonx**: Granite 3 8B Instruct LLM
- **FAISS**: Facebook AI Similarity Search

### APIs
- **IBM Cloud IAM**: Authentication
- **IBM Watsonx API**: LLM inference

## Performance Characteristics

### Offline Mode
- **Speed**: <100ms per query
- **Accuracy**: Depends on database coverage
- **Cost**: Zero (no API calls)
- **Availability**: 100% (no internet needed)

### Online Mode
- **Speed**: 2-5 seconds per query
- **Accuracy**: Higher (LLM reasoning)
- **Cost**: Per API call
- **Availability**: Requires internet + API access

### Scalability
- **Current**: ~1000 Q&A pairs
- **Recommended**: Up to 100K entries
- **For larger**: Use FAISS IVF index

## Security Considerations

1. **API Keys**: Stored in .env (not committed)
2. **Access Control**: IBM Cloud IAM
3. **Data Privacy**: Local processing for offline mode
4. **Input Validation**: Query sanitization

## Future Enhancements

1. **Multilingual Support**: Hindi, regional languages
2. **Voice Input**: Speech-to-text for farmers
3. **Feedback Loop**: User ratings to improve answers
4. **Advanced FAISS**: IVF index for larger datasets
5. **Caching**: Cache frequent queries
6. **Analytics**: Query logging and insights
7. **Mobile App**: Native mobile interface
8. **Offline LLM**: Local model for complete offline operation

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
- **Streamlit Cloud**: Easy deployment
- **Docker**: Containerized deployment
- **AWS/Azure/GCP**: Cloud hosting
- **On-premise**: For data privacy

## Monitoring & Maintenance

### Key Metrics
- Query response time
- FAISS retrieval accuracy
- LLM API success rate
- User satisfaction scores

### Maintenance Tasks
- Update Q&A database regularly
- Monitor API usage and costs
- Retrain embeddings if model updated
- Rebuild FAISS index periodically

## References

- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [IBM Watsonx](https://www.ibm.com/watsonx)
- [Streamlit Docs](https://docs.streamlit.io/)
