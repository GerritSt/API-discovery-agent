"""
API Discovery Agent
This module provides functionality to discover and extract API documentation for companies.
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class APIDiscoveryAgent:
    """Agent to discover and extract API documentation for companies."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_for_api_documentation(self, company_name: str) -> Optional[str]:
        """
        Search for API documentation URL for a given company.
        
        Args:
            company_name: Name of the company or software
            
        Returns:
            URL of the API documentation if found, None otherwise
        """
        logger.info(f"Searching for API documentation for: {company_name}")
        
        # Common patterns for API documentation URLs
        search_patterns = [
            f"{company_name} api documentation",
            f"{company_name} api reference",
            f"{company_name} developer documentation",
            f"{company_name} api docs"
        ]
        
        # Try common URL patterns first
        common_domains = [
            f"https://api.{company_name.lower().replace(' ', '')}.com",
            f"https://developer.{company_name.lower().replace(' ', '')}.com",
            f"https://docs.{company_name.lower().replace(' ', '')}.com",
            f"https://{company_name.lower().replace(' ', '')}.com/api",
            f"https://{company_name.lower().replace(' ', '')}.com/docs",
            f"https://{company_name.lower().replace(' ', '')}.com/developers",
            f"https://www.{company_name.lower().replace(' ', '')}.com/api",
        ]
        
        for url in common_domains:
            try:
                response = self.session.get(url, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    # Check if the page contains API-related content
                    soup = BeautifulSoup(response.text, 'lxml')
                    text = soup.get_text().lower()
                    if any(keyword in text for keyword in ['api', 'endpoint', 'rest', 'graphql', 'documentation']):
                        logger.info(f"Found API documentation at: {url}")
                        return url
            except Exception as e:
                logger.debug(f"Could not access {url}: {str(e)}")
                continue
        
        logger.warning(f"Could not find API documentation for {company_name}")
        return None
    
    def extract_endpoints(self, url: str) -> List[Dict[str, str]]:
        """
        Extract API endpoints from documentation page.
        
        Args:
            url: URL of the API documentation
            
        Returns:
            List of endpoint dictionaries with details
        """
        logger.info(f"Extracting endpoints from: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            endpoints = []
            
            # Strategy 1: Look for common API endpoint patterns in code blocks
            code_blocks = soup.find_all(['code', 'pre'])
            for block in code_blocks:
                text = block.get_text()
                # Find HTTP method and path patterns
                matches = re.findall(r'(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+(/[\w\-/{}:]*)', text, re.IGNORECASE)
                for method, path in matches:
                    endpoint = self._create_endpoint_dict(method.upper(), path, block)
                    if endpoint not in endpoints:
                        endpoints.append(endpoint)
            
            # Strategy 2: Look for endpoint documentation in structured format
            # Check for tables with endpoint information
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        cell_text = ' '.join([cell.get_text().strip() for cell in cells])
                        matches = re.findall(r'(GET|POST|PUT|DELETE|PATCH)\s+(/[\w\-/{}:]*)', cell_text, re.IGNORECASE)
                        for method, path in matches:
                            endpoint = self._create_endpoint_dict(method.upper(), path, row)
                            if endpoint not in endpoints:
                                endpoints.append(endpoint)
            
            # Strategy 3: Look for API paths in links and headings
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']):
                text = tag.get_text()
                # Look for paths that start with /api, /v1, etc.
                matches = re.findall(r'(GET|POST|PUT|DELETE|PATCH)?\s*(/api[\w\-/{}:]*|/v\d+[\w\-/{}:]*)', text, re.IGNORECASE)
                for method, path in matches:
                    if not method:
                        method = 'GET'  # Default to GET if not specified
                    endpoint = self._create_endpoint_dict(method.upper(), path, tag)
                    if endpoint not in endpoints:
                        endpoints.append(endpoint)
            
            # Strategy 4: Look for URL patterns in the page
            all_text = soup.get_text()
            url_patterns = re.findall(r'(GET|POST|PUT|DELETE|PATCH)\s+(https?://[^\s]+/api[^\s]*)', all_text, re.IGNORECASE)
            for method, full_url in url_patterns:
                parsed = urlparse(full_url)
                path = parsed.path
                endpoint = self._create_endpoint_dict(method.upper(), path, None)
                if endpoint not in endpoints:
                    endpoints.append(endpoint)
            
            if not endpoints:
                logger.warning(f"No endpoints found at {url}")
            else:
                logger.info(f"Found {len(endpoints)} endpoints")
            
            return endpoints
            
        except Exception as e:
            logger.error(f"Error extracting endpoints from {url}: {str(e)}")
            return []
    
    def _create_endpoint_dict(self, method: str, path: str, element) -> Dict[str, str]:
        """Create a standardized endpoint dictionary."""
        # Extract description from surrounding context if available
        description = ""
        if element:
            # Try to find description in parent or sibling elements
            parent = element.parent if hasattr(element, 'parent') else None
            if parent:
                description = parent.get_text().strip()[:200]  # Limit to 200 chars
        
        return {
            'method': method,
            'path': path.strip(),
            'description': description,
            'full_endpoint': f"{method} {path.strip()}"
        }
    
    def discover_api(self, company_name: str) -> Tuple[Optional[str], List[Dict[str, str]]]:
        """
        Main method to discover API documentation and extract endpoints.
        
        Args:
            company_name: Name of the company or software
            
        Returns:
            Tuple of (documentation_url, list_of_endpoints)
        """
        doc_url = self.search_for_api_documentation(company_name)
        
        if not doc_url:
            return None, []
        
        endpoints = self.extract_endpoints(doc_url)
        return doc_url, endpoints
