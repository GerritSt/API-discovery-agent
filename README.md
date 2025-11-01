# API Discovery Agent

An automated workflow agent that discovers, documents, and tabulates a company's API documentation into Excel files.

## Overview

This Python application automatically:
1. Searches for a company's API documentation
2. Extracts available endpoints and their details
3. Saves the structured information to an Excel spreadsheet

## Features

- **Automatic API Discovery**: Searches common URL patterns to find API documentation
- **Endpoint Extraction**: Parses documentation pages to extract HTTP methods, paths, and descriptions
- **Excel Export**: Creates well-formatted, filterable Excel spreadsheets with:
  - Color-coded headers
  - Auto-adjusted column widths
  - Frozen header rows
  - Alternating row colors for readability
  - Metadata (documentation URL, timestamp, endpoint count)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GerritSt/API-discovery-agent.git
cd API-discovery-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Search for a company's API and generate documentation:

```bash
python main.py "CompanyName"
```

### Advanced Options

Specify output filename:
```bash
python main.py "GitHub" --output github_api.xlsx
```

Enable verbose logging:
```bash
python main.py "Stripe" --verbose
```

### Command Line Options

- `company` (required): Name of the company or software to search for
- `-o, --output`: Custom output Excel filename (optional)
- `-v, --verbose`: Enable verbose logging for debugging

### Examples

```bash
# Search for Stripe API
python main.py "Stripe"

# Search for GitHub API with custom output
python main.py "GitHub" --output github_docs.xlsx

# Search with verbose logging
python main.py "Twilio" --verbose
```

## Output

The application generates an Excel file containing:

- **Company Name**: The searched company
- **Documentation URL**: Link to the official API documentation
- **Endpoint List**: Table with columns:
  - Method (GET, POST, PUT, DELETE, etc.)
  - Path (e.g., `/api/v1/users`)
  - Full Endpoint (combined method and path)
  - Description (extracted from documentation)
  - Notes (empty column for user annotations)

## Requirements

- Python 3.12+
- Internet connection (to access API documentation)
- Dependencies listed in `requirements.txt`:
  - requests
  - beautifulsoup4
  - openpyxl
  - lxml
  - urllib3

## How It Works

1. **Search Phase**: The agent tries common URL patterns:
   - `https://api.{company}.com`
   - `https://developer.{company}.com`
   - `https://docs.{company}.com`
   - `https://{company}.com/api`
   - And more...

2. **Extraction Phase**: Uses multiple strategies to find endpoints:
   - Parses code blocks for HTTP methods and paths
   - Scans tables for structured endpoint data
   - Analyzes headings and links for API paths
   - Detects URL patterns in text

3. **Export Phase**: Creates a formatted Excel spreadsheet with all findings

## Limitations

- Requires publicly accessible API documentation
- Extraction accuracy depends on documentation structure
- Some APIs may require authentication to view documentation
- Complex or non-standard documentation formats may not be fully parsed

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for use and modification.
