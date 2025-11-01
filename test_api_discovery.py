"""
Unit tests for API Discovery Agent
"""

import unittest
import os
from api_discovery import APIDiscoveryAgent
from excel_exporter import ExcelExporter
from openpyxl import load_workbook


class TestExcelExporter(unittest.TestCase):
    """Test the Excel export functionality."""
    
    def test_create_spreadsheet(self):
        """Test creating an Excel spreadsheet with sample data."""
        exporter = ExcelExporter()
        
        sample_endpoints = [
            {
                'method': 'GET',
                'path': '/api/v1/test',
                'full_endpoint': 'GET /api/v1/test',
                'description': 'Test endpoint'
            }
        ]
        
        output_file = exporter.create_spreadsheet(
            company_name="TestCompany",
            doc_url="https://test.com/api/docs",
            endpoints=sample_endpoints,
            filename="test_output.xlsx"
        )
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Verify content
        wb = load_workbook(output_file)
        sheet = wb.active
        
        # Check title
        self.assertIn("TestCompany", sheet['A1'].value)
        
        # Check URL
        self.assertEqual("https://test.com/api/docs", sheet['B2'].value)
        
        # Check endpoint count
        self.assertEqual(1, sheet['B3'].value)
        
        # Check headers
        self.assertEqual("Method", sheet['A6'].value)
        self.assertEqual("Path", sheet['B6'].value)
        
        # Check data
        self.assertEqual("GET", sheet['A7'].value)
        self.assertEqual("/api/v1/test", sheet['B7'].value)
        
        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)


class TestAPIDiscoveryAgent(unittest.TestCase):
    """Test the API Discovery Agent functionality."""
    
    def test_create_endpoint_dict(self):
        """Test endpoint dictionary creation."""
        agent = APIDiscoveryAgent()
        
        endpoint = agent._create_endpoint_dict('GET', '/api/test', None)
        
        self.assertEqual('GET', endpoint['method'])
        self.assertEqual('/api/test', endpoint['path'])
        self.assertEqual('GET /api/test', endpoint['full_endpoint'])
        self.assertIsInstance(endpoint['description'], str)


if __name__ == '__main__':
    unittest.main()
