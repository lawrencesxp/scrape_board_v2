from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper import main as scrape_file

app = Flask(__name__, static_folder='../frontend')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        scraped_data = scrape_file(url)
        return jsonify(scraped_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)