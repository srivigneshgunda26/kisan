# 🌾 START HERE - Kisan Call Centre Query Assistant

## 👋 Welcome!

Your Kisan Call Centre Query Assistant is ready to build! Follow these simple steps.

---

## 🚀 Step-by-Step Instructions

### Step 1️⃣: Install Python Packages (1 minute)

Open your terminal/command prompt in this folder and run:

```bash
pip install -r requirements.txt
```

**What this does**: Installs all necessary AI libraries (Streamlit, FAISS, Sentence Transformers, etc.)

---

### Step 2️⃣: Setup the System (2-3 minutes)

Run the setup script:

```bash
python setup.py
```

**What this does**:
- ✓ Processes the sample agricultural Q&A data
- ✓ Generates AI embeddings for semantic search
- ✓ Creates FAISS index for fast retrieval
- ✓ Prepares everything for the application

**Expected output**:
```
============================================================
Kisan Call Centre Query Assistant - Setup
============================================================

Step 1: Data Preprocessing
...
✓ Data preprocessing completed

Step 2: Generating Embeddings
...
✓ Embeddings generated successfully

Step 3: Creating FAISS Index
...
✓ FAISS index created successfully

✓ Setup completed successfully!
============================================================
```

---

### Step 3️⃣: Launch the Application (instant)

Start the web application:

```bash
streamlit run app.py
```

**What this does**: Opens the Kisan Call Centre Assistant in your web browser

**You'll see**: A beautiful web interface at http://localhost:8501

---

## 🎯 Using the Application

### Try These Sample Queries:

1. **Pest Control**
   ```
   How to control aphids in mustard?
   ```

2. **Disease Management**
   ```
   What is the treatment for leaf spot in tomato?
   ```

3. **Fertilizer Advice**
   ```
   What fertilizer is recommended during flowering in maize?
   ```

4. **Government Schemes**
   ```
   How to apply for PM Kisan Samman Nidhi scheme?
   ```

### What You'll See:

**Two Answers for Each Query:**

📚 **Offline Answer** (Left side)
- Fast retrieval from KCC database
- Shows matching Q&A pairs
- Works without internet

🤖 **Online Answer** (Right side)
- AI-generated using OpenRouter LLM
- Natural language response
- Context-aware and detailed

---

## ✅ Your System is Pre-Configured

✓ **OpenRouter API Key**: Already set in `.env` file
✓ **LLM Model**: Free Llama 3.1 (no cost)
✓ **Sample Data**: Included for testing
✓ **All Scripts**: Ready to run

---

## 📁 Project Files Overview

```
📦 Your Project
│
├── 🚀 START_HERE.md          ← You are here!
├── 📖 QUICKSTART.md          ← Quick 3-step guide
├── 📚 README.md              ← Project overview
│
├── 🎯 app.py                 ← Main application
├── ⚙️ setup.py               ← Setup script
├── 🧪 test_system.py         ← Test everything
│
├── 📂 scripts/               ← Data processing
├── 📂 utils/                 ← Core utilities
├── 📂 data/                  ← Sample data
│
└── 📖 Documentation/
    ├── SETUP_GUIDE.md        ← Detailed setup
    ├── USAGE_GUIDE.md        ← How to use
    ├── ARCHITECTURE.md       ← Technical details
    └── PROJECT_SUMMARY.md    ← Complete overview
```

---

## 🔧 Troubleshooting

### Problem: "No module named 'streamlit'"
**Solution**: Run `pip install -r requirements.txt`

### Problem: "data/raw_kcc.csv not found"
**Solution**: The setup script will use sample data automatically

### Problem: "Port 8501 already in use"
**Solution**: Run `streamlit run app.py --server.port 8502`

### Problem: Something else?
**Solution**: Run the test script:
```bash
python test_system.py
```

---

## 🎓 Learning Resources

### Quick Reference
- **QUICKSTART.md** - Get started in 3 steps
- **USAGE_GUIDE.md** - Learn all features

### Detailed Guides
- **SETUP_GUIDE.md** - Installation details
- **ARCHITECTURE.md** - How it works
- **PROJECT_SUMMARY.md** - Complete overview

---

## 🎉 Ready to Start?

### Run These 3 Commands:

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Setup system
python setup.py

# 3. Launch app
streamlit run app.py
```

---

## 💡 What Makes This Special?

✨ **Dual-Mode System**
- Works offline (FAISS search)
- Enhanced online (AI generation)

🚀 **Fast & Accurate**
- Semantic search in milliseconds
- Context-aware AI responses

🌾 **Built for Farmers**
- Simple interface
- Agricultural expertise
- Practical advice

🆓 **Free to Use**
- Open source
- Free LLM model
- No hidden costs

---

## 📞 Need Help?

1. Check the documentation files
2. Run `python test_system.py`
3. Review error messages carefully
4. Ensure all dependencies installed

---

## 🎯 Your Next Steps

1. ✅ Run `pip install -r requirements.txt`
2. ✅ Run `python setup.py`
3. ✅ Run `streamlit run app.py`
4. ✅ Try sample queries
5. ✅ Explore the features!

---

**🌾 Built for Indian Farmers | 🤖 Powered by AI | 🇮🇳 Made with ❤️**

---

## 🚀 Let's Get Started!

Open your terminal and run the first command:

```bash
pip install -r requirements.txt
```

**Good luck! 🎉**
