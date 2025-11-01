#!/usr/bin/env python3
"""
Demo script for API Discovery Agent
Demonstrates functionality with mock data when internet is not available.
"""

import sys
from excel_exporter import ExcelExporter

def create_demo_documentation():
    """Create a demo Excel file with sample API endpoints."""
    
    print("=" * 70)
    print("API Discovery Agent - Demo Mode")
    print("=" * 70)
    print("Creating demo documentation with sample data...")
    print()
    
    # Sample company data
    company_name = "ExampleCorp"
    doc_url = "https://api.examplecorp.com/docs"
    
    # Sample endpoints
    sample_endpoints = [
        {
            'method': 'GET',
            'path': '/api/v1/users',
            'full_endpoint': 'GET /api/v1/users',
            'description': 'Retrieve a list of all users. Supports pagination and filtering.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/users/{id}',
            'full_endpoint': 'GET /api/v1/users/{id}',
            'description': 'Get details for a specific user by ID.'
        },
        {
            'method': 'POST',
            'path': '/api/v1/users',
            'full_endpoint': 'POST /api/v1/users',
            'description': 'Create a new user account. Requires authentication.'
        },
        {
            'method': 'PUT',
            'path': '/api/v1/users/{id}',
            'full_endpoint': 'PUT /api/v1/users/{id}',
            'description': 'Update an existing user. Requires authentication and appropriate permissions.'
        },
        {
            'method': 'DELETE',
            'path': '/api/v1/users/{id}',
            'full_endpoint': 'DELETE /api/v1/users/{id}',
            'description': 'Delete a user account. This action is irreversible.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/products',
            'full_endpoint': 'GET /api/v1/products',
            'description': 'Retrieve all products. Supports filtering by category, price range, and availability.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/products/{id}',
            'full_endpoint': 'GET /api/v1/products/{id}',
            'description': 'Get detailed information about a specific product.'
        },
        {
            'method': 'POST',
            'path': '/api/v1/products',
            'full_endpoint': 'POST /api/v1/products',
            'description': 'Create a new product listing. Requires admin authentication.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/orders',
            'full_endpoint': 'GET /api/v1/orders',
            'description': 'Retrieve order history. Returns orders for the authenticated user.'
        },
        {
            'method': 'POST',
            'path': '/api/v1/orders',
            'full_endpoint': 'POST /api/v1/orders',
            'description': 'Create a new order. Processes payment and inventory allocation.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/orders/{id}',
            'full_endpoint': 'GET /api/v1/orders/{id}',
            'description': 'Get details of a specific order including status and tracking.'
        },
        {
            'method': 'PATCH',
            'path': '/api/v1/orders/{id}',
            'full_endpoint': 'PATCH /api/v1/orders/{id}',
            'description': 'Update order status or shipping information.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/auth/login',
            'full_endpoint': 'GET /api/v1/auth/login',
            'description': 'Authenticate user and return access token.'
        },
        {
            'method': 'POST',
            'path': '/api/v1/auth/logout',
            'full_endpoint': 'POST /api/v1/auth/logout',
            'description': 'Invalidate current session token.'
        },
        {
            'method': 'GET',
            'path': '/api/v1/search',
            'full_endpoint': 'GET /api/v1/search',
            'description': 'Search across users, products, and orders. Supports full-text search.'
        }
    ]
    
    # Create the Excel file
    exporter = ExcelExporter()
    output_file = exporter.create_spreadsheet(
        company_name=company_name,
        doc_url=doc_url,
        endpoints=sample_endpoints,
        filename="ExampleCorp_API_Documentation_Demo.xlsx"
    )
    
    print(f"✓ Demo Excel file created: {output_file}")
    print(f"✓ Total sample endpoints: {len(sample_endpoints)}")
    print(f"✓ Documentation URL: {doc_url}")
    print()
    print("=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70)
    print()
    print("You can now:")
    print("  1. Open the Excel file to see the formatted output")
    print("  2. Review the main.py for the full implementation")
    print("  3. Run main.py with a real company name when internet is available")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(create_demo_documentation())
