# Quick Start Guide - Kisan Call Centre Query Assistant

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Setup the System (2-3 minutes)
```bash
python setup.py
```

This will:
- ✓ Process the sample KCC dataset
- ✓ Generate embeddings using Sentence Transformer
- ✓ Create FAISS index for fast search

### Step 3: Launch the App (instant)
```bash
streamlit run app.py
```

Your browser will open automatically at: http://localhost:8501

## ✅ You're Ready!

The system is pre-configured with:
- ✓ OpenRouter API key (already set in .env)
- ✓ Sample agricultural Q&A data
- ✓ Free Llama 3.1 model

## 🎯 Try These Queries

Click on any sample query in the sidebar, or type:

1. **Pest Control**
   - "How to control aphids in mustard?"
   - "Suggest pesticide for whitefly in cotton"

2. **Disease Management**
   - "What is the treatment for leaf spot in tomato?"
   - "How to treat blight in potato crops?"

3. **Fertilizer Guidance**
   - "What fertilizer is recommended during flowering in maize?"

4. **Government Schemes**
   - "How to apply for PM Kisan Samman Nidhi scheme?"

## 📊 What You'll See

The app shows TWO answers for each query:

1. **Offline Answer** (Left side)
   - Fast retrieval from KCC database
   - Shows top matching Q&A pairs
   - Works without internet

2. **Online Answer** (Right side)
   - AI-generated using OpenRouter LLM
   - Context-aware and natural
   - Enhanced accuracy

## 🔧 Troubleshooting

### Issue: Import errors
```bash
pip install -r requirements.txt
```

### Issue: Setup fails
```bash
# Check if data file exists
dir data

# Re-run setup
python setup.py
```

### Issue: Port already in use
```bash
streamlit run app.py --server.port 8502
```

## 📚 Next Steps

- Add your own KCC data to `data/raw_kcc.csv`
- Run `python setup.py` again to process new data
- Explore the documentation:
  - `USAGE_GUIDE.md` - Detailed usage instructions
  - `ARCHITECTURE.md` - Technical details
  - `SETUP_GUIDE.md` - Advanced configuration

## 🎉 That's It!

You now have a fully functional AI-powered agricultural helpdesk running locally.

---

**Need Help?** Run the test script:
```bash
python test_system.py
```
