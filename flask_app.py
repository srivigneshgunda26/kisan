"""
Flask Application for Kisan Call Centre Query Assistant
Enhanced with visualizations and better response generation
"""
from flask import Flask, render_template, request, jsonify, session
from utils.query_handler import QueryHandler
from utils.llm_client import GraniteLLMClient
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize handlers
query_handler = None
llm_client = None

def initialize_system():
    """Initialize query handler and LLM client"""
    global query_handler, llm_client
    
    try:
        if query_handler is None:
            query_handler = QueryHandler()
            print("✓ Query handler initialized")
        
        if llm_client is None and os.path.exists('.env'):
            try:
                llm_client = GraniteLLMClient()
                print("✓ LLM client initialized")
            except Exception as e:
                print(f"⚠ LLM client not available: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return False

# Initialize on startup
initialize_system()

# Store query history
query_history = []

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process user query and return results"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        online_mode = data.get('online_mode', True)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Retrieve from FAISS
        results = query_handler.retrieve_top_k(query, k=5)
        
        if not results:
            return jsonify({'error': 'No relevant information found'}), 404
        
        # Format offline answer
        offline_answer = query_handler.format_offline_answer(results)
        
        # Generate online answer if enabled
        online_answer = None
        if online_mode and llm_client:
            try:
                context = query_handler.format_context_for_llm(results)
                online_answer = llm_client.generate_answer(query, context)
                print(f"✓ Generated AI answer ({len(online_answer)} chars)")
            except Exception as e:
                error_msg = f"Error generating AI response: {str(e)}"
                print(f"❌ {error_msg}")
                online_answer = error_msg
        
        # Extract categories and crops for visualization
        categories = {}
        crops = {}
        for result in results:
            cat = result.get('category', 'General')
            crop = result.get('crop', 'General')
            categories[cat] = categories.get(cat, 0) + 1
            crops[crop] = crops.get(crop, 0) + 1
        
        # Store in history
        query_entry = {
            'query': query,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results_count': len(results),
            'categories': list(categories.keys()),
            'crops': list(crops.keys())
        }
        query_history.append(query_entry)
        
        # Keep only last 50 queries
        if len(query_history) > 50:
            query_history.pop(0)
        
        response = {
            'success': True,
            'query': query,
            'offline_answer': offline_answer,
            'online_answer': online_answer,
            'results': results[:3],  # Top 3 results
            'statistics': {
                'total_results': len(results),
                'categories': categories,
                'crops': crops,
                'avg_distance': sum(r['distance'] for r in results) / len(results)
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def get_statistics():
    """Get overall system statistics"""
    try:
        # Get database stats
        total_entries = query_handler.index.ntotal if query_handler else 0
        
        # Analyze query history
        total_queries = len(query_history)
        recent_queries = query_history[-10:] if query_history else []
        
        # Category distribution from metadata
        all_categories = {}
        all_crops = {}
        if query_handler and query_handler.metadata:
            for entry in query_handler.metadata:
                cat = entry.get('category', 'General')
                crop = entry.get('crop', 'General')
                all_categories[cat] = all_categories.get(cat, 0) + 1
                all_crops[crop] = all_crops.get(crop, 0) + 1
        
        return jsonify({
            'success': True,
            'total_entries': total_entries,
            'total_queries': total_queries,
            'recent_queries': recent_queries,
            'categories': all_categories,
            'crops': all_crops
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-queries')
def get_sample_queries():
    """Get sample queries"""
    samples = [
        {
            'query': 'How to control aphids in mustard?',
            'category': 'Pest Control',
            'icon': '🐛'
        },
        {
            'query': 'What is the treatment for leaf spot in tomato?',
            'category': 'Disease Management',
            'icon': '🦠'
        },
        {
            'query': 'Suggest pesticide for whitefly in cotton',
            'category': 'Pest Control',
            'icon': '🐛'
        },
        {
            'query': 'What fertilizer is recommended during flowering in maize?',
            'category': 'Fertilizer',
            'icon': '🌱'
        },
        {
            'query': 'How to apply for PM Kisan Samman Nidhi scheme?',
            'category': 'Government Schemes',
            'icon': '📋'
        },
        {
            'query': 'How to protect paddy from blast disease?',
            'category': 'Disease Management',
            'icon': '🦠'
        }
    ]
    return jsonify(samples)

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
