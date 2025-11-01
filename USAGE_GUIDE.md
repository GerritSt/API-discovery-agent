# API Discovery Agent - Usage Guide

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/GerritSt/API-discovery-agent.git
cd API-discovery-agent

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Basic Usage
```bash
python main.py "CompanyName"
```

This will:
1. Search for the company's API documentation
2. Extract all available endpoints
3. Create an Excel file with the results

#### With Custom Output
```bash
python main.py "GitHub" --output my_github_docs.xlsx
```

#### With Verbose Logging
```bash
python main.py "Stripe" --verbose
```

### Demo Mode

If you don't have internet access or want to see a sample output:

```bash
python demo.py
```

This creates a sample Excel file with mock API endpoint data.

## Understanding the Output

The generated Excel file contains:

### Header Section
- **Title**: Company name and "API Documentation"
- **Documentation URL**: Link to the official API docs
- **Total Endpoints**: Number of endpoints found
- **Generated**: Timestamp of when the file was created

### Endpoint Table
Each row represents an API endpoint with:

1. **Method**: HTTP method (GET, POST, PUT, DELETE, PATCH, etc.)
2. **Path**: The endpoint path (e.g., `/api/v1/users`)
3. **Full Endpoint**: Combined method and path
4. **Description**: Information about what the endpoint does
5. **Notes**: Empty column for your own annotations

### Features
- **Sortable/Filterable**: Excel auto-filter enabled on all columns
- **Color-coded**: Headers are blue, alternating row colors for readability
- **Frozen headers**: Headers stay visible when scrolling
- **Auto-sized columns**: Columns automatically adjusted for content

## Tips for Best Results

### Company Names
- Use the official company name or common abbreviation
- Examples: "Stripe", "GitHub", "Twilio", "SendGrid"
- Try variations if the first attempt doesn't work

### Common Issues

**Issue**: "Could not find API documentation"
- The company may not have publicly accessible API docs
- Try the full company name or abbreviation
- Check if the company actually provides a public API

**Issue**: "No endpoints were automatically extracted"
- The documentation was found but endpoint extraction failed
- The Excel file will still contain the documentation URL
- Manually visit the URL to view the endpoints

**Issue**: "Connection errors"
- Check your internet connection
- Some sites may block automated requests
- Try again after a short wait

## Architecture

The application consists of three main modules:

### 1. api_discovery.py
- Searches for API documentation using common URL patterns
- Extracts endpoints from HTML using multiple strategies:
  - Code block parsing
  - Table scanning
  - Heading and link analysis
  - URL pattern detection

### 2. excel_exporter.py
- Creates formatted Excel spreadsheets
- Applies styling and formatting
- Generates metadata and headers

### 3. main.py
- Command-line interface
- Orchestrates the discovery and export process
- Error handling and user feedback

## Testing

Run the unit tests:
```bash
python -m unittest test_api_discovery.py -v
```

## Dependencies

- **requests**: HTTP requests to fetch documentation
- **beautifulsoup4**: HTML parsing and data extraction
- **openpyxl**: Excel file creation and formatting
- **lxml**: Fast HTML/XML processing
- **urllib3**: HTTP client library

## Examples

### Example 1: E-commerce Platform
```bash
python main.py "Shopify"
```

Expected output:
- File: `Shopify_API_Documentation_YYYYMMDD_HHMMSS.xlsx`
- Contains endpoints for products, orders, customers, etc.

### Example 2: Payment Gateway
```bash
python main.py "Stripe" --output stripe_endpoints.xlsx
```

Expected output:
- File: `stripe_endpoints.xlsx`
- Contains endpoints for payments, customers, subscriptions, etc.

### Example 3: Cloud Service
```bash
python main.py "AWS" --verbose
```

Expected output:
- Detailed logging of the search and extraction process
- File with AWS API endpoints (if documentation is accessible)

## Extending the Application

### Adding Custom Search Patterns

Edit `api_discovery.py` and add patterns to `search_for_api_documentation()`:

```python
common_domains = [
    f"https://api.{company_name}.com",
    f"https://your-custom-pattern.{company_name}.com",
    # Add more patterns
]
```

### Improving Endpoint Extraction

Edit the `extract_endpoints()` method to add new extraction strategies.

### Customizing Excel Output

Edit `excel_exporter.py` to change:
- Color schemes
- Column widths
- Additional metadata
- Sheet layouts

## Troubleshooting

### Problem: Module not found
```bash
pip install -r requirements.txt
```

### Problem: Permission denied
```bash
chmod +x main.py demo.py
```

### Problem: Excel file won't open
- Make sure openpyxl is installed correctly
- Check file permissions in the output directory

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Open source - free to use and modify.