#!/usr/bin/env python3
"""
AI API Discovery Agent - Main Entry Point
Uses FREE DeepSeek AI to intelligently discover and document company APIs.
"""

import argparse
import sys
import logging
from ai_api_discovery import AIAPIDiscovery
from excel_exporter import ExcelExporter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the AI API Discovery Agent."""
    
    parser = argparse.ArgumentParser(
        description='AI API Discovery Agent - Use FREE DeepSeek AI to find and document company APIs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py "Stripe"
  python main.py "GitHub" --output github_api.xlsx
  python main.py "Twilio" --verbose

Note: Requires OPENROUTER_API_KEY environment variable to be set.
Get a FREE API key at: https://openrouter.ai/keys
        '''
    )
    
    parser.add_argument(
        'company',
        type=str,
        help='Company name to search for API documentation'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output Excel filename (auto-generated if not provided)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Header
    logger.info("=" * 70)
    logger.info("AI API Discovery Agent (FREE DeepSeek AI)")
    logger.info("=" * 70)
    logger.info(f"Searching for: {args.company}")
    logger.info("")
    
    try:
        # Initialize AI agent
        logger.info("Step 1: Using FREE DeepSeek AI to search for API documentation...")
        agent = AIAPIDiscovery()
        
        # Search for API
        api_info = agent.search_company_api(args.company)
        
        # Check results
        if not api_info.get('has_api'):
            logger.error(f"❌ No public API found for '{args.company}'")
            if api_info.get('error'):
                logger.error(f"Error: {api_info['error']}")
            logger.info("\nThe AI could not find a public API for this company.")
            logger.info("This could mean:")
            logger.info("  - The company doesn't have a public API")
            logger.info("  - The API information is not publicly available")
            logger.info("  - The company name might need to be more specific")
            sys.exit(1)
        
        # Display results
        logger.info(f"✓ Found API information")
        logger.info(f"  Main Documentation: {api_info['main_documentation_url']}")
        logger.info(f"  API Type: {api_info['api_type']}")
        logger.info(f"  Description: {api_info['description']}")
        
        if api_info.get('documentation_pages'):
            logger.info(f"  Documentation Pages: {len(api_info['documentation_pages'])} found")
        logger.info("")
        
        # Export to Excel
        logger.info("Step 2: Creating Excel spreadsheet...")
        exporter = ExcelExporter()
        output_file = exporter.create_spreadsheet(api_info, filename=args.output)
        
        logger.info(f"✓ Excel file created: {output_file}")
        logger.info("")
        
        # Summary
        logger.info("=" * 70)
        logger.info("✅ Success! API information has been saved to Excel.")
        logger.info("=" * 70)
        logger.info(f"Company: {api_info['company_name']}")
        logger.info(f"API Type: {api_info['api_type']}")
        logger.info(f"Documentation Pages: {len(api_info.get('documentation_pages', []))}")
        logger.info(f"Output File: {output_file}")
        logger.info("=" * 70)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n\n⚠ Operation cancelled by user")
        return 130
        
    except Exception as e:
        logger.error(f"\n❌ An error occurred: {str(e)}")
        if args.verbose:
            logger.exception("Full error details:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
