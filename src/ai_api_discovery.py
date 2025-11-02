"""
AI-powered API Discovery Agent
Uses OpenRouter's DeepSeek AI (free) to intelligently search for company APIs and documentation.
"""

import os
import requests
import json
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class AIAPIDiscovery:
    """AI-powered agent that uses DeepSeek AI to discover company APIs."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI API Discovery agent.
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-chat-v3.1:free"
        logger.info("AI API Discovery agent initialized with DeepSeek v3.1")
        
    def search_company_api(self, company_name: str) -> Dict:
        """
        Use AI to search for a company's API documentation.
        
        Args:
            company_name: Name of the company to search for
            
        Returns:
            Dictionary with API information
        """
        logger.info(f"Searching for {company_name} API using AI...")
        
        prompt = f"""Find the actual API endpoints for {company_name}'s public API. I need:
1. Does the company have a public API? (Yes/No)
2. A list of the main API endpoints with their HTTP methods, paths, and descriptions
3. API type (REST, GraphQL, SOAP, etc.)
4. Base URL for the API

Respond ONLY with valid JSON in this exact format:
{{
    "company_name": "{company_name}",
    "has_api": true,
    "api_type": "REST",
    "base_url": "https://api.example.com/v1",
    "endpoints": [
        {{"method": "GET", "path": "/users", "description": "Retrieve list of users"}},
        {{"method": "POST", "path": "/users", "description": "Create a new user"}},
        {{"method": "GET", "path": "/users/{{id}}", "description": "Get user by ID"}},
        {{"method": "PUT", "path": "/users/{{id}}", "description": "Update user"}},
        {{"method": "DELETE", "path": "/users/{{id}}", "description": "Delete user"}}
    ]
}}

Provide at least 10-15 of the most important/commonly used endpoints if available.
If no public API exists, set has_api to false and use empty strings/arrays."""

        try:
            # Make API request to OpenRouter
            response = requests.post(
                url=self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/GerritSt/API-discovery-agent",
                    "X-Title": "API Discovery Agent"
                },
                data=json.dumps({
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert at finding API documentation. Provide accurate, current URLs. Respond only with valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract content from response
            content = response_data['choices'][0]['message']['content'].strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            logger.info(f"Successfully found API info for {company_name}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return self._empty_result(company_name, f"JSON parse error: {str(e)}")
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response body: {e.response.text}")
            return self._empty_result(company_name, f"API request error: {str(e)}")
        except Exception as e:
            logger.error(f"Error searching for {company_name} API: {e}")
            return self._empty_result(company_name, str(e))
    
    def _empty_result(self, company_name: str, error: str = "") -> Dict:
        """Return an empty result structure."""
        return {
            "company_name": company_name,
            "has_api": False,
            "api_type": "",
            "base_url": "",
            "endpoints": [],
            "error": error
        }

if __name__ == "__main__":
    # Simple example usage
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    agent = AIAPIDiscovery()
    
    company = input("Enter company name: ")
    result = agent.search_company_api(company)
    
    print("\n" + "=" * 70)
    print(f"Company: {result['company_name']}")
    print(f"Has API: {result['has_api']}")
    
    if result['has_api']:
        print(f"\nAPI Type: {result['api_type']}")
        print(f"Base URL: {result['base_url']}")
        
        if result['endpoints']:
            print(f"\nAPI Endpoints ({len(result['endpoints'])}):")
            for endpoint in result['endpoints']:
                print(f"  {endpoint['method']:<7} {endpoint['path']:<40} - {endpoint['description']}")
    else:
        print("No public API found")
        if result.get('error'):
            print(f"Error: {result['error']}")
    
    print("=" * 70)