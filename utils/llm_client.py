"""
Milestone 4: LLM Integration
Connects to Google Gemini API for LLM inference
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GraniteLLMClient:
    def __init__(self):
        """
        Initialize Google Gemini LLM client
        """
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'gemini-2.5-flash')
        
        if not self.api_key:
            raise ValueError("Missing Google API key. Check .env file")
        
        # Use v1 API instead of v1beta
        self.endpoint = f"https://generativelanguage.googleapis.com/v1/models/{self.model_name}:generateContent?key={self.api_key}"
        
        print(f"LLM Client initialized with Google Gemini: {self.model_name}")
    
    def generate_answer(self, query, context):
        """
        Generate answer using Google Gemini
        """
        # Create prompt
        prompt = f"""You are an agricultural expert assistant for Indian farmers. Use the provided context to answer the farmer's question accurately and helpfully.

Context from Kisan Call Centre database:
{context}

Farmer's Question: {query}

IMPORTANT: 
1. Provide your answer in ENGLISH language only.
2. Format your response clearly with:
   - Use numbered lists (1., 2., 3.) for steps or multiple options
   - Use bullet points for sub-items
   - Keep sentences clear and concise
   - Include specific measurements and dosages
   - Add practical tips when relevant

Based on the context above, provide a clear, practical answer. If the context doesn't fully address the question, supplement with your agricultural knowledge. Keep the answer actionable and farmer-friendly."""
        
        # Prepare request
        headers = {
            "Content-Type": "application/json"
        }
        
        body = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        try:
            # Make request
            response = requests.post(self.endpoint, headers=headers, json=body, timeout=30)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            # Check if response has the expected structure
            if 'candidates' not in result or len(result['candidates']) == 0:
                raise Exception("No response generated from Gemini API")
            
            candidate = result['candidates'][0]
            
            # Check for content filtering or other issues
            if 'content' not in candidate:
                finish_reason = candidate.get('finishReason', 'UNKNOWN')
                if finish_reason == 'SAFETY':
                    raise Exception("Response blocked by safety filters")
                elif finish_reason == 'MAX_TOKENS':
                    raise Exception("Response truncated due to length limit")
                else:
                    raise Exception(f"No content in response. Finish reason: {finish_reason}")
            
            generated_text = candidate['content']['parts'][0]['text']
            
            # Validate the response is not empty
            if not generated_text or len(generated_text.strip()) < 10:
                raise Exception("Generated response is too short or empty")
            
            return generated_text.strip()
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nResponse: {e.response.text}"
            raise Exception(error_msg)
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected response format: missing key {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")

