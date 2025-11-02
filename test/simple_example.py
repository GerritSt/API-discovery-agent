#!/usr/bin/env python3
"""
Simple standalone example - FREE DeepSeek AI API Discovery
This shows the minimal code needed to use the agent.
"""

import os
import sys

# Add src to path
sys.path.insert(0, 'src')

from ai_api_discovery import AIAPIDiscovery
from excel_exporter import ExcelExporter

# Set your API key here or use environment variable
# Get FREE key from: https://openrouter.ai/keys
os.environ['OPENROUTER_API_KEY'] = 'your-api-key-here'  # Replace this!

# Search for a company's API
company = "Stripe"
print(f"Searching for {company} API using FREE DeepSeek AI...")

agent = AIAPIDiscovery()
result = agent.search_company_api(company)

# Display results
print("\n" + "=" * 70)
if result['has_api']:
    print(f"✓ Found {company} API!")
    print(f"Type: {result['api_type']}")
    print(f"Main URL: {result['main_documentation_url']}")
    print(f"\nDocumentation Pages ({len(result['documentation_pages'])}):")
    for page in result['documentation_pages']:
        print(f"  - {page['title']}: {page['url']}")
    
    # Export to Excel
    exporter = ExcelExporter()
    output = exporter.create_spreadsheet(result)
    print(f"\n✓ Excel saved to: {output}")
else:
    print(f"✗ No API found for {company}")
print("=" * 70)
