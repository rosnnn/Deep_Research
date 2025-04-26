import re
from tavily import TavilyClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class ResearchAgent:
    def __init__(self, query, max_results=3):
        self.query = query
        self.max_results = max_results
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("API Key for Tavily not found in the .env file.")
        
        self.client = TavilyClient(api_key=self.api_key)
        self.collected_texts = []

    def gather_information(self):
        print(f"\n[🔎] ResearchAgent: Searching for '{self.query}' using Tavily API...")
        try:
            # Perform the search using Tavily API
            response = self.client.search(
                query=self.query,
                max_results=self.max_results,
                search_depth="basic"
            )
            
            # Extract results
            results = response.get("results", [])
            for result in results:
                url = result.get("url", "No URL")
                content = result.get("content", "")
                
                if content:
                    # Clean and ensure complete content
                    cleaned_content = self.clean_content(content)

                    # Append the cleaned content if it is valid
                    if cleaned_content:
                        self.collected_texts.append({
                            "url": url,
                            "text": cleaned_content
                        })
            
            print(f"[✅] Collected from {len(self.collected_texts)} sources.")
            return self.collected_texts

        except Exception as e:
            print(f"[⚠️] Failed to search with Tavily API: {e}")
            return []

    def clean_content(self, content):
        # Apply a regex to ensure full sentences are captured
        sentences = re.split(r'(?<=\.)\s+', content)  # Split content into sentences by periods.
        cleaned_content = " ".join(sentences).strip()
        
        # If content length exceeds threshold, truncate it gracefully at the last full sentence
        if len(cleaned_content) > 16000:
            cleaned_content = cleaned_content[:16000]

        # If content seems too short or fragmented, discard it
        if len(cleaned_content) < 50:  # Set a threshold to ignore fragments
            return None
        
        return cleaned_content
