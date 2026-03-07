"""
Milestone 5: Streamlit UI
Main application interface for Kisan Call Centre Query Assistant
"""
import streamlit as st
import os
from utils.query_handler import QueryHandler
from utils.llm_client import GraniteLLMClient

# Page configuration
st.set_page_config(
    page_title="Kisan Call Centre Query Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E7D32;
        padding: 20px;
    }
    .query-box {
        background-color: #F1F8E9;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .answer-box {
        background-color: #E8F5E9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .offline-answer {
        border-left: 4px solid #4CAF50;
    }
    .online-answer {
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'query_handler' not in st.session_state:
    st.session_state.query_handler = None
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = None

def initialize_system():
    """Initialize query handler and LLM client"""
    try:
        if st.session_state.query_handler is None:
            with st.spinner("Loading AI models..."):
                st.session_state.query_handler = QueryHandler()
        
        if st.session_state.llm_client is None and os.path.exists('.env'):
            try:
                st.session_state.llm_client = GraniteLLMClient()
            except Exception as e:
                st.warning(f"LLM client not available: {str(e)}")
        
        return True
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return False

def main():
    # Header
    st.markdown("<h1 class='main-header'>🌾 Kisan Call Centre Query Assistant</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>AI-Powered Agricultural Helpdesk using Google Gemini Flash and FAISS</p>", 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🌾 Kisan Call Centre")
        st.markdown("---")
        
        st.markdown("### About")
        st.info("""
        This AI assistant helps farmers with:
        - Crop disease management
        - Pest control solutions
        - Fertilizer recommendations
        - Government scheme information
        """)
        
        st.markdown("### Sample Queries")
        sample_queries = [
            "How to control aphids in mustard?",
            "What is the treatment for leaf spot in tomato?",
            "How to apply for PM Kisan Samman Nidhi scheme?",
            "What fertilizer is recommended during flowering in maize?",
            "How to protect paddy from blast disease?"
        ]
        
        for query in sample_queries:
            if st.button(query, key=query, use_container_width=True):
                st.session_state.sample_query = query
        
        st.markdown("---")
        online_mode = st.checkbox("Enable Online Mode (LLM)", 
                                  value=True,
                                  help="Use Google Gemini Flash for enhanced answers")
        
        if online_mode:
            st.success("✓ Gemini Flash Active")
    
    # Initialize system
    if not initialize_system():
        st.stop()
    
    # Main content
    st.markdown("### Ask Your Agricultural Query")
    
    # Query input
    query = st.text_area(
        "Enter your question:",
        value=st.session_state.get('sample_query', ''),
        height=100,
        placeholder="Example: How to control aphids in mustard crop?"
    )
    
    # Clear sample query after use
    if 'sample_query' in st.session_state:
        del st.session_state.sample_query
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    # Process query
    if search_button and query.strip():
        with st.spinner("Searching knowledge base..."):
            # Retrieve from FAISS
            results = st.session_state.query_handler.retrieve_top_k(query, k=5)
            
            if results:
                # Display results in two columns
                col_left, col_right = st.columns(2)
                
                # Offline Answer
                with col_left:
                    st.markdown("### 📚 Offline Answer")
                    st.markdown("<div class='answer-box offline-answer'>", 
                              unsafe_allow_html=True)
                    
                    offline_answer = st.session_state.query_handler.format_offline_answer(results)
                    st.write(offline_answer)
                    
                    with st.expander("View Retrieved Entries"):
                        for i, result in enumerate(results[:3], 1):
                            st.markdown(f"**Entry {i}:**")
                            st.markdown(f"*Q: {result['question']}*")
                            st.markdown(f"A: {result['answer']}")
                            st.markdown(f"*Category: {result.get('category', 'N/A')} | Crop: {result.get('crop', 'N/A')}*")
                            st.markdown("---")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Online Answer
                with col_right:
                    st.markdown("### 🤖 Online Answer (AI Generated)")
                    st.markdown("<div class='answer-box online-answer'>", 
                              unsafe_allow_html=True)
                    
                    if online_mode and st.session_state.llm_client:
                        with st.spinner("Generating AI response..."):
                            try:
                                context = st.session_state.query_handler.format_context_for_llm(results)
                                online_answer = st.session_state.llm_client.generate_answer(query, context)
                                st.write(online_answer)
                            except Exception as e:
                                st.error(f"Error generating online answer: {str(e)}")
                                st.info("Showing offline answer only.")
                    else:
                        st.info("Online mode is disabled or LLM client not configured. Enable it in the sidebar and ensure .env file is set up correctly.")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No relevant information found. Please try rephrasing your query.")
    
    elif search_button:
        st.warning("Please enter a query to search.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Powered by Google Gemini Flash & FAISS | Built for Indian Farmers 🇮🇳</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
