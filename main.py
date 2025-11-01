#!/usr/bin/env python3
"""
API Discovery Agent - Main Entry Point
Automatically discovers and documents company APIs into Excel spreadsheets.
"""

import argparse
import sys
import logging
from api_discovery import APIDiscoveryAgent
from excel_exporter import ExcelExporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the API Discovery Agent."""
    
    parser = argparse.ArgumentParser(
        description='API Discovery Agent - Automatically discover and document company APIs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py "Stripe"
  python main.py "GitHub" --output github_api.xlsx
  python main.py "Twilio" --verbose
        '''
    )
    
    parser.add_argument(
        'company',
        type=str,
        help='Name of the company or software to search for API documentation'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output Excel filename (optional, auto-generated if not provided)'
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
    
    logger.info("=" * 70)
    logger.info("API Discovery Agent")
    logger.info("=" * 70)
    logger.info(f"Searching for: {args.company}")
    logger.info("")
    
    try:
        # Initialize the agent
        agent = APIDiscoveryAgent()
        
        # Discover API documentation
        logger.info("Step 1: Searching for API documentation...")
        doc_url, endpoints = agent.discover_api(args.company)
        
        if not doc_url:
            logger.error(f"❌ Could not find API documentation for '{args.company}'")
            logger.info("\nTips:")
            logger.info("  - Make sure the company name is spelled correctly")
            logger.info("  - Try using the full company name or common abbreviation")
            logger.info("  - Some companies may not have publicly accessible APIs")
            sys.exit(1)
        
        logger.info(f"✓ Found API documentation: {doc_url}")
        logger.info("")
        
        # Check if endpoints were found
        if not endpoints:
            logger.warning(f"⚠ No endpoints were automatically extracted from the documentation")
            logger.info(f"The documentation URL has been found, but endpoint extraction failed.")
            logger.info(f"You can manually review the documentation at: {doc_url}")
            
            # Create a minimal spreadsheet with just the URL
            endpoints = [{
                'method': 'N/A',
                'path': 'N/A',
                'full_endpoint': 'See documentation URL above',
                'description': f'Automatic extraction failed. Please visit {doc_url} to view endpoints.'
            }]
        else:
            logger.info(f"Step 2: Extracting endpoint information...")
            logger.info(f"✓ Extracted {len(endpoints)} endpoints")
            logger.info("")
        
        # Export to Excel
        logger.info("Step 3: Creating Excel spreadsheet...")
        exporter = ExcelExporter()
        output_file = exporter.create_spreadsheet(
            company_name=args.company,
            doc_url=doc_url,
            endpoints=endpoints,
            filename=args.output
        )
        
        logger.info(f"✓ Excel file created: {output_file}")
        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ Success! API documentation has been saved to Excel.")
        logger.info("=" * 70)
        logger.info(f"Output file: {output_file}")
        logger.info(f"Total endpoints: {len(endpoints)}")
        logger.info(f"Documentation URL: {doc_url}")
        
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
