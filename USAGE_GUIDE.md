# Kisan Call Centre Query Assistant - Usage Guide

## Getting Started

### Step 1: Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Setup the System

```bash
# Run the complete setup
python setup.py
```

This will:
- Process the KCC dataset
- Generate embeddings
- Create FAISS index

### Step 3: Configure IBM Watsonx (Optional)

For online mode with LLM:

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Add your credentials:
```
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

Access at: http://localhost:8501

## Using the Application

### Main Interface

1. **Query Input**: Enter your agricultural question
2. **Sample Queries**: Click sidebar buttons for examples
3. **Search Button**: Process your query
4. **Results**: View offline and online answers

### Features

#### Offline Mode
- Fast retrieval from KCC database
- Works without internet
- Shows top matching Q&A pairs
- Expandable details for each result

#### Online Mode
- AI-generated answers using IBM Watsonx
- Context-aware responses
- Natural language output
- Enhanced accuracy

### Sample Queries

#### Pest Control
```
How to control aphids in mustard?
Suggest pesticide for whitefly in cotton
How to prevent fruit borer in brinjal?
```

#### Disease Management
```
What is the treatment for leaf spot in tomato?
How to protect paddy from blast disease?
How to treat blight in potato crops?
```

#### Fertilizer Guidance
```
What fertilizer is recommended during flowering in maize?
What is the dosage of neem oil for aphids?
```

#### Government Schemes
```
How to apply for PM Kisan Samman Nidhi scheme?
```

## Advanced Usage

### Adding Your Own Data

1. Prepare CSV file with columns:
   - `QueryText`: The question
   - `KccAns`: The answer
   - `Category`, `Crop`, `QueryType`: Optional metadata

2. Save as `data/raw_kcc.csv`

3. Run setup:
```bash
python setup.py
```

### Customizing Retrieval

Edit `utils/query_handler.py`:

```python
# Change number of results
results = handler.retrieve_top_k(query, k=10)  # Default: 5

# Adjust answer formatting
# Modify format_offline_answer() method
```

### Customizing LLM Behavior

Edit `utils/llm_client.py`:

```python
# Adjust generation parameters
"parameters": {
    "temperature": 0.7,      # Creativity (0.0-1.0)
    "max_new_tokens": 500,   # Response length
    "top_p": 0.9,            # Nucleus sampling
}

# Modify prompt template
prompt = f"""Your custom prompt here..."""
```

### Running Individual Scripts

#### Preprocess Data Only
```bash
python scripts/preprocess_data.py
```

#### Generate Embeddings Only
```bash
python scripts/generate_embeddings.py
```

#### Create FAISS Index Only
```bash
python scripts/create_faiss_index.py
```

## Testing

### Run System Tests
```bash
python test_system.py
```

This checks:
- Package installations
- Data file existence
- Query handler functionality
- LLM client configuration

### Manual Testing

1. Start the app
2. Try sample queries
3. Check both offline and online answers
4. Verify response quality

## Troubleshooting

### Common Issues

#### 1. Import Errors
```
Error: No module named 'sentence_transformers'
```
**Solution**: 
```bash
pip install -r requirements.txt
```

#### 2. Data Not Found
```
Error: data/raw_kcc.csv not found
```
**Solution**: 
- Add your dataset to `data/raw_kcc.csv`
- Or use sample data: `cp data/sample_raw_kcc.csv data/raw_kcc.csv`

#### 3. FAISS Index Error
```
Error: models/faiss_index.bin not found
```
**Solution**: 
```bash
python setup.py
```

#### 4. LLM API Error
```
Error: Missing IBM Watsonx credentials
```
**Solution**: 
- Create `.env` file with credentials
- Or use offline mode only (disable online mode in UI)

#### 5. Streamlit Port Busy
```
Error: Port 8501 already in use
```
**Solution**: 
```bash
streamlit run app.py --server.port 8502
```

### Performance Issues

#### Slow Embedding Generation
- Use GPU if available
- Reduce batch size in `generate_embeddings.py`
- Process data in chunks

#### Slow FAISS Search
- Use FAISS GPU version: `pip install faiss-gpu`
- Consider IVF index for large datasets
- Reduce `k` parameter in retrieval

#### LLM Timeout
- Check internet connection
- Verify API credentials
- Reduce `max_new_tokens` parameter

## Best Practices

### Data Quality
1. Clean and validate input data
2. Remove duplicates
3. Standardize text format
4. Include diverse examples

### Query Formulation
1. Be specific in questions
2. Include crop/pest names
3. Mention context (season, region)
4. Use simple language

### System Maintenance
1. Update Q&A database regularly
2. Monitor API usage and costs
3. Rebuild embeddings after data updates
4. Test with new queries periodically

## API Usage and Costs

### IBM Watsonx Pricing
- Pay per token generated
- Free tier available
- Monitor usage in IBM Cloud dashboard

### Optimization Tips
1. Use offline mode when possible
2. Cache frequent queries
3. Limit `max_new_tokens`
4. Batch similar queries

## Integration Options

### As a Web Service
```python
# Create REST API wrapper
from flask import Flask, request, jsonify
from utils.query_handler import QueryHandler

app = Flask(__name__)
handler = QueryHandler()

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json['query']
    results = handler.retrieve_top_k(user_query)
    return jsonify(results)
```

### As a Python Library
```python
# Use in your own scripts
from utils.query_handler import QueryHandler
from utils.llm_client import GraniteLLMClient

handler = QueryHandler()
llm = GraniteLLMClient()

# Get answer
results = handler.retrieve_top_k("How to control aphids?")
context = handler.format_context_for_llm(results)
answer = llm.generate_answer("How to control aphids?", context)
```

### As a Chatbot
- Integrate with WhatsApp/Telegram
- Add conversation history
- Support voice input
- Multilingual support

## Extending the System

### Add New Features

#### 1. Multilingual Support
```python
# Add translation layer
from googletrans import Translator

translator = Translator()
query_en = translator.translate(query, dest='en').text
```

#### 2. Voice Input
```python
# Add speech recognition
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.listen(source)
    query = recognizer.recognize_google(audio)
```

#### 3. Feedback System
```python
# Add rating mechanism
if st.button("👍 Helpful"):
    save_feedback(query, answer, rating=1)
if st.button("👎 Not Helpful"):
    save_feedback(query, answer, rating=0)
```

#### 4. Query Analytics
```python
# Log queries for analysis
import logging

logging.info(f"Query: {query}, Results: {len(results)}")
```

## Support and Resources

### Documentation
- README.md: Project overview
- SETUP_GUIDE.md: Installation instructions
- ARCHITECTURE.md: Technical details
- This file: Usage guide

### External Resources
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [IBM Watsonx Docs](https://www.ibm.com/docs/en/watsonx)
- [Streamlit Docs](https://docs.streamlit.io/)

### Getting Help
1. Check documentation files
2. Run test script: `python test_system.py`
3. Review error messages carefully
4. Verify all dependencies installed

## Contributing

To improve the system:
1. Add more Q&A data
2. Test with diverse queries
3. Optimize performance
4. Add new features
5. Improve UI/UX

## License

MIT License - Feel free to use and modify for your needs.
