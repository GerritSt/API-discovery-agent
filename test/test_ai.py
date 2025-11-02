#!/usr/bin/env python3
"""
Simple test script for AI API Discovery (FREE DeepSeek AI)
Run this to verify the AI-powered discovery is working.
"""

import sys
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Add src to path (go up one directory, then into src)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from ai_api_discovery import AIAPIDiscovery
from excel_exporter import ExcelExporter

def test_ai_discovery():
    """Test the AI discovery with a well-known API."""
    
    print("=" * 70)
    print("Testing AI API Discovery Agent (FREE DeepSeek AI)")
    print("=" * 70)
    print()
    
    # Check for API key
    if not os.getenv('OPENROUTER_API_KEY'):
        print("WARNING: OPENROUTER_API_KEY environment variable not set!")
        print("Please set it before running:")
        print("  Windows: set OPENROUTER_API_KEY=your-key-here")
        print("  Linux/Mac: export OPENROUTER_API_KEY=your-key-here")
        print("\nGet a FREE API key at: https://openrouter.ai/keys")
        return
    
    try:
        # Initialize agent
        print("Initializing AI agent...")
        agent = AIAPIDiscovery()
        
        # Test with Stripe (well-known API)
        company = "Stripe"
        print(f"\nSearching for {company} API using AI...")
        result = agent.search_company_api(company)
        
        # Display results
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Company: {result['company_name']}")
        print(f"Has API: {result['has_api']}")
        
        if result['has_api']:
            print(f"API Type: {result['api_type']}")
            print(f"Base URL: {result['base_url']}")
            print(f"\nAPI Endpoints ({len(result['endpoints'])}):")
            for i, endpoint in enumerate(result['endpoints'], 1):
                print(f"  {i}. {endpoint['method']:<7} {endpoint['path']}")
                print(f"      {endpoint['description']}")
            
            # Test Excel export
            print("\n" + "=" * 70)
            print("Testing Excel Export...")
            exporter = ExcelExporter()
            output_file = exporter.create_spreadsheet(result)
            print(f"Excel file created: {output_file}")
            print("=" * 70)
            print("\nAll tests passed!")
        else:
            print("No API found")
            if result.get('error'):
                print(f"Error: {result['error']}")
    
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_discovery()
