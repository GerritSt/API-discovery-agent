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
        Use AI to search for a company's API endpoints using iterative discovery.
        
        Args:
            company_name: Name of the company to search for
            
        Returns:
            Dictionary with API information
        """
        logger.info(f"Searching for {company_name} API using AI...")
        
        # First pass: Get initial batch of endpoints
        result = self._fetch_endpoints(company_name)
        
        if not result.get('has_api'):
            return result
        
        # Ensure base_url is present (some salvaged JSON might be missing it)
        if not result.get('base_url'):
            result['base_url'] = 'N/A'
        if not result.get('api_type'):
            result['api_type'] = 'REST'
        if not result.get('company_name'):
            result['company_name'] = company_name
        
        # If we got endpoints, try to get more in additional passes
        all_endpoints = result.get('endpoints', [])
        max_iterations = 5  # Limit iterations to prevent infinite loops
        iteration = 1
        
        while iteration < max_iterations:
            logger.info(f"Fetching additional endpoints (iteration {iteration + 1})...")
            additional_result = self._fetch_additional_endpoints(company_name, all_endpoints)
            
            new_endpoints = additional_result.get('endpoints', [])
            if not new_endpoints:
                logger.info("No more endpoints found")
                break
            
            # Add only unique endpoints
            existing_paths = {f"{ep['method']}:{ep['path']}" for ep in all_endpoints}
            unique_new = [ep for ep in new_endpoints 
                         if f"{ep['method']}:{ep['path']}" not in existing_paths]
            
            if not unique_new:
                logger.info("No new unique endpoints found")
                break
            
            all_endpoints.extend(unique_new)
            logger.info(f"Added {len(unique_new)} new endpoints. Total: {len(all_endpoints)}")
            iteration += 1
        
        result['endpoints'] = all_endpoints
        logger.info(f"Successfully found {len(all_endpoints)} API endpoints for {company_name}")
        return result
    
    def _fetch_endpoints(self, company_name: str) -> Dict:
        """Fetch initial batch of endpoints."""
        prompt = '''Find the actual API endpoints for ''' + company_name + ''''s public API. I need:
1. Does the company have a public API? (Yes/No)
2. A list of the main API endpoints with their HTTP methods, paths, descriptions, and parameters
3. API type (REST, GraphQL, SOAP, etc.)
4. Base URL for the API

Respond ONLY with valid JSON in this exact format:
{
    "company_name": "''' + company_name + '''",
    "has_api": true,
    "api_type": "REST",
    "base_url": "https://api.example.com/v1",
    "endpoints": [
        {"method": "GET", "path": "/users", "description": "Retrieve list of users", "parameters": [{"name": "limit", "type": "integer"}, {"name": "offset", "type": "integer"}]},
        {"method": "POST", "path": "/users", "description": "Create a new user", "parameters": [{"name": "email", "type": "string"}, {"name": "name", "type": "string"}]},
        {"method": "GET", "path": "/users/{id}", "description": "Get user by ID", "parameters": [{"name": "id", "type": "string"}]},
        {"method": "PUT", "path": "/users/{id}", "description": "Update user", "parameters": [{"name": "id", "type": "string"}, {"name": "name", "type": "string"}]},
        {"method": "DELETE", "path": "/users/{id}", "description": "Delete user", "parameters": [{"name": "id", "type": "string"}]}
    ]
}

For each endpoint, include the key parameters with their name and data type (string, integer, boolean, array, object, etc.).
Provide 15-20 of the most important/commonly used endpoints.
If no public API exists, set has_api to false and use empty strings/arrays.'''

        return self._make_api_request(prompt, company_name)
    
    def _fetch_additional_endpoints(self, company_name: str, existing_endpoints: List[Dict]) -> Dict:
        """Fetch additional endpoints not in the existing list."""
        # Create a summary of existing endpoints (show first 30)
        existing_summary = "\n".join([f"- {ep['method']} {ep['path']}" for ep in existing_endpoints[:30]])
        
        prompt = f'''I already have these {len(existing_endpoints)} endpoints for {company_name}'s API:

{existing_summary}
{"..." if len(existing_endpoints) > 30 else ""}

Find 15-20 MORE API endpoints that are NOT in the list above. Focus on different resource types and operations.

Respond ONLY with valid JSON in this exact format:
{{
    "endpoints": [
        {{"method": "GET", "path": "/invoices", "description": "List all invoices", "parameters": [{{"name": "limit", "type": "integer"}}, {{"name": "status", "type": "string"}}]}},
        {{"method": "POST", "path": "/invoices", "description": "Create an invoice", "parameters": [{{"name": "customer_id", "type": "string"}}, {{"name": "amount", "type": "integer"}}]}}
    ]
}}

For each endpoint, include the key parameters with their name and data type (string, integer, boolean, array, object, etc.).
Only include NEW endpoints that are different from the list above. If there are no more endpoints, return an empty endpoints array.'''

        return self._make_api_request(prompt, company_name)
    
    def _make_api_request(self, prompt: str, company_name: str) -> Dict:
        """
        Make API request to AI model.
        
        Args:
            prompt: The prompt to send to the AI
            company_name: Name of the company being searched
            
        Returns:
            Dictionary with API information or error
        """
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
                            "content": "You are an expert at finding API documentation. Provide accurate, current endpoints. Respond ONLY with valid JSON. Do not add any explanatory text, comments, or markdown formatting outside the JSON structure."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1  # Lower temperature for more consistent JSON output
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
            
            # Clean up common JSON issues
            content = self._clean_json_response(content)
            
            result = json.loads(content)
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.debug(f"Problematic content (first 500 chars): {content[:500]}")
            
            # Try to salvage partial JSON
            salvaged = self._salvage_json(content)
            if salvaged:
                logger.info("Successfully recovered partial JSON data")
                return salvaged
            
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
    
    def _clean_json_response(self, content: str) -> str:
        """Clean up common JSON formatting issues from AI responses."""
        # Remove any trailing commas before closing brackets/braces
        import re
        content = re.sub(r',\s*}', '}', content)
        content = re.sub(r',\s*]', ']', content)
        
        # Remove any comments (// or /* */)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        return content.strip()
    
    def _salvage_json(self, content: str) -> Optional[Dict]:
        """Try to salvage partial JSON from malformed response."""
        try:
            # Try to find the first complete JSON object
            import re
            
            # Look for JSON object pattern
            json_match = re.search(r'\{[\s\S]*\}', content)
            if not json_match:
                return None
            
            json_str = json_match.group(0)
            
            # Try progressively smaller chunks if parsing fails
            lines = json_str.split('\n')
            for i in range(len(lines), 0, -1):
                try:
                    partial = '\n'.join(lines[:i])
                    # Try to close any open braces/brackets
                    open_braces = partial.count('{') - partial.count('}')
                    open_brackets = partial.count('[') - partial.count(']')
                    
                    # Add missing closing characters
                    partial += ']' * open_brackets + '}' * open_braces
                    
                    # Clean and parse
                    partial = self._clean_json_response(partial)
                    result = json.loads(partial)
                    return result
                except:
                    continue
            
            return None
        except Exception as e:
            logger.debug(f"Failed to salvage JSON: {e}")
            return None

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
                params = endpoint.get('parameters', [])
                param_str = ", ".join([f"{p['name']} ({p['type']})" for p in params]) if params else "None"
                print(f"  {endpoint['method']:<7} {endpoint['path']:<40} - {endpoint['description']}")
                print(f"          Parameters: {param_str}")
    else:
        print("No public API found")
        if result.get('error'):
            print(f"Error: {result['error']}")
    
    print("=" * 70)