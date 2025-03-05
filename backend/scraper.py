import os
import requests
import pandas as pd
import io
import json
import numpy as np
from urllib.parse import urlparse

def detect_file_type(url):
    """Detect file type based on URL or file extension"""
    parsed_url = urlparse(url)
    file_extension = os.path.splitext(parsed_url.path)[1].lower()
    
    extension_map = {
        '.csv': 'csv',
        '.xls': 'excel',
        '.xlsx': 'excel',
        '.pdf': 'pdf'
    }
    
    return extension_map.get(file_extension, 'unknown')

def scrape_file(url):
    """Scrape file based on its type"""
    try:
        # Add headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        file_type = detect_file_type(url)
        
        if file_type == 'csv':
            # Try multiple encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(
                        io.StringIO(response.text), 
                        encoding=encoding, 
                        low_memory=False,
                        on_bad_lines='skip'  # Skip problematic lines
                    )
                    
                    # Clean column names
                    df.columns = [col.strip() for col in df.columns]
                    
                    # Replace NaN with None for JSON serialization
                    df = df.replace({np.nan: None})
                    
                    # Convert to records
                    return df.to_dict(orient='records')
                except Exception as e:
                    print(f"Failed with {encoding} encoding: {e}")
                    continue
            
            return [{"error": "Could not parse CSV with any encoding"}]
        
        elif file_type == 'excel':
            # Use pandas to read Excel
            df = pd.read_excel(io.BytesIO(response.content))
            
            # Replace NaN with None for JSON serialization
            df = df.replace({np.nan: None})
            
            return df.to_dict(orient='records')
        
        elif file_type == 'pdf':
            # For PDF, you'd need additional libraries like PyPDF2 or pdfplumber
            return [{"error": "PDF parsing not implemented"}]
        
        else:
            return [{"error": "Unsupported file type"}]
    
    except requests.RequestException as e:
        return [{"error": f"Request failed: {str(e)}"}]
    except Exception as e:
        return [{"error": str(e)}]

def main(url):
    """Main scraping function"""
    return scrape_file(url)

if __name__ == "__main__":
    # Example usage
    url = input("Enter the URL of the file to scrape: ")
    result = main(url)
    print(result)