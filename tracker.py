from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import time

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# Store tracked products in memory
products = {}

@app.route('/add-product', methods=['POST'])
def add_product():
    """Add a product to track"""
    data = request.json
    asin = data.get('asin')
    
    if not asin:
        return jsonify({'error': 'ASIN required'}), 400
    
    products[asin] = {
        'asin': asin,
        'current_rank': None,
        'previous_rank': None,
        'last_checked': None
    }
    
    return jsonify({'message': 'Product added', 'asin': asin})

@app.route('/check-rank/<asin>', methods=['GET'])
def check_rank(asin):
    """Check the rank of a specific product"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        url = f'https://www.amazon.com/dp/{asin}'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch product page'}), 500
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Look for "Best Sellers Rank" text
        rank = None
        bsr_section = soup.find('th', string=re.compile('Best Sellers Rank', re.IGNORECASE))
        
        if bsr_section:
            rank_cell = bsr_section.find_next('td')
            if rank_cell:
                rank_match = re.search(r'#([\d,]+)', rank_cell.text)
                if rank_match:
                    rank = int(rank_match.group(1).replace(',', ''))
        
        # Method 2: Try product details section
        if not rank:
            detail_bullets = soup.find('div', {'id': 'detailBullets_feature_div'})
            if detail_bullets:
                rank_match = re.search(r'Best Sellers Rank.*?#([\d,]+)', detail_bullets.text, re.DOTALL)
                if rank_match:
                    rank = int(rank_match.group(1).replace(',', ''))
        
        if rank:
            # Update stored data
            if asin in products:
                products[asin]['previous_rank'] = products[asin]['current_rank']
                products[asin]['current_rank'] = rank
                products[asin]['last_checked'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return jsonify({
                'asin': asin,
                'rank': rank,
                'previous_rank': products.get(asin, {}).get('previous_rank'),
                'last_checked': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({'error': 'Could not find rank on page'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['GET'])
def get_products():
    """Get all tracked products"""
    return jsonify(products)

@app.route('/remove-product/<asin>', methods=['DELETE'])
def remove_product(asin):
    """Remove a product from tracking"""
    if asin in products:
        del products[asin]
        return jsonify({'message': 'Product removed'})
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    print("🚀 Amazon Rank Tracker Server Starting...")
    print("📡 Server running on http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    app.run(debug=True, port=5000)