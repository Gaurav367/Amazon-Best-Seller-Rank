from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import time
import random

app = Flask(__name__)
CORS(app)

products = {}

# Rotate user agents to avoid detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

@app.route('/add-product', methods=['POST'])
def add_product():
    """Add a product to track"""
    data = request.json
    asin = data.get('asin')
    
    if not asin:
        return jsonify({'error': 'ASIN required'}), 400
    
    products[asin] = {
        'asin': asin,
        'current_ranks': [],
        'previous_ranks': [],
        'last_checked': None
    }
    
    return jsonify({'message': 'Product added', 'asin': asin})

@app.route('/check-rank/<asin>', methods=['GET'])
def check_rank(asin):
    """Check all ranks for a specific product"""
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        
        url = f'https://www.amazon.com/dp/{asin}'
        
        # Add random delay to seem more human-like
        time.sleep(random.uniform(0.5, 1.5))
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        print(f"Status Code for {asin}: {response.status_code}")
        
        if response.status_code != 200:
            return jsonify({'error': f'Failed to fetch product page (Status: {response.status_code})'}), 500
        
        soup = BeautifulSoup(response.content, 'html.parser')
        ranks = []
        
        # DEBUG: Save page content for inspection
        # with open(f'debug_{asin}.html', 'w', encoding='utf-8') as f:
        #     f.write(soup.prettify())
        
        # Method 1: productDetails_detailBullets_sections1
        detail_section = soup.find('div', {'id': 'productDetails_detailBullets_sections1'})
        if detail_section:
            print(f"Found productDetails_detailBullets_sections1 for {asin}")
            ranks.extend(parse_detail_section(detail_section))
        
        # Method 2: detailBullets_feature_div
        if not ranks:
            detail_bullets = soup.find('div', {'id': 'detailBullets_feature_div'})
            if detail_bullets:
                print(f"Found detailBullets_feature_div for {asin}")
                ranks.extend(parse_detail_bullets(detail_bullets))
        
        # Method 3: Product details table (th/td)
        if not ranks:
            tables = soup.find_all('table', {'class': ['prodDetTable', 'a-normal', 'a-spacing-micro']})
            for table in tables:
                print(f"Checking table for {asin}")
                ranks.extend(parse_table(table))
                if ranks:
                    break
        
        # Method 4: Search for any text containing "Best Sellers Rank"
        if not ranks:
            bsr_text = soup.find_all(string=re.compile(r'Best Sellers Rank', re.IGNORECASE))
            for text_elem in bsr_text:
                print(f"Found BSR text for {asin}")
                parent = text_elem.parent
                # Get surrounding context
                for _ in range(3):  # Check up to 3 parent levels
                    if parent:
                        ranks.extend(parse_text_content(parent.get_text()))
                        if ranks:
                            break
                        parent = parent.parent
                if ranks:
                    break
        
        # Method 5: Look in all spans/divs for rank patterns
        if not ranks:
            all_text = soup.get_text()
            print(f"Parsing full page text for {asin}")
            ranks.extend(parse_text_content(all_text))
        
        # Remove duplicates
        ranks = remove_duplicates(ranks)
        
        print(f"Found {len(ranks)} ranks for {asin}: {ranks}")
        
        if ranks:
            # Update stored data
            if asin in products:
                products[asin]['previous_ranks'] = products[asin]['current_ranks']
                products[asin]['current_ranks'] = ranks
                products[asin]['last_checked'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            return jsonify({
                'asin': asin,
                'ranks': ranks,
                'previous_ranks': products.get(asin, {}).get('previous_ranks', []),
                'last_checked': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            print(f"No ranks found for {asin}")
            return jsonify({'error': 'Could not find any ranks on page', 'debug': 'Check if ASIN is valid or if Amazon is blocking requests'}), 404
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout - Amazon may be slow'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

def parse_detail_section(section):
    """Parse productDetails_detailBullets_sections1"""
    ranks = []
    
    # Look for all tr elements
    rows = section.find_all('tr')
    for row in rows:
        th = row.find('th')
        td = row.find('td')
        
        if th and td:
            if 'Best Sellers Rank' in th.get_text():
                text = td.get_text()
                ranks.extend(extract_ranks_from_text(text))
    
    return ranks

def parse_detail_bullets(section):
    """Parse detailBullets_feature_div"""
    ranks = []
    text = section.get_text()
    ranks.extend(extract_ranks_from_text(text))
    return ranks

def parse_table(table):
    """Parse product details table"""
    ranks = []
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all(['th', 'td'])
        for cell in cells:
            if 'Best Sellers Rank' in cell.get_text():
                # Get next sibling or parent text
                text = row.get_text()
                ranks.extend(extract_ranks_from_text(text))
    
    return ranks

def parse_text_content(text):
    """Parse any text content for ranks"""
    return extract_ranks_from_text(text)

def extract_ranks_from_text(text):
    """Extract all rank patterns from text"""
    ranks = []
    
    # Pattern 1: #123,456 in Category Name
    pattern1 = r'#([\d,]+)\s+in\s+([^\n(#]+?)(?:\s*\(|$|\n)'
    matches1 = re.finditer(pattern1, text, re.IGNORECASE)
    
    for match in matches1:
        try:
            rank_num = int(match.group(1).replace(',', ''))
            category = match.group(2).strip()
            
            # Clean up category name
            category = re.sub(r'\s+', ' ', category)
            category = category.split('(')[0].strip()
            
            # Validate category
            if category and len(category) > 3 and len(category) < 150:
                # Skip if it's just a link or "See Top 100"
                if not re.search(r'^(See|Top|Learn|Shop)', category, re.IGNORECASE):
                    ranks.append({
                        'rank': rank_num,
                        'category': category
                    })
        except (ValueError, IndexError):
            continue
    
    return ranks

def remove_duplicates(ranks):
    """Remove duplicate ranks"""
    seen = set()
    unique_ranks = []
    
    for rank_info in ranks:
        # Create a key from rank and first 50 chars of category
        key = (rank_info['rank'], rank_info['category'][:50])
        if key not in seen:
            seen.add(key)
            unique_ranks.append(rank_info)
    
    return unique_ranks

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

@app.route('/test/<asin>', methods=['GET'])
def test_scrape(asin):
    """Test endpoint to debug scraping"""
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        url = f'https://www.amazon.com/dp/{asin}'
        response = requests.get(url, headers=headers, timeout=15)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        debug_file = f'debug_{asin}.html'
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        return jsonify({
            'message': f'HTML saved to {debug_file}',
            'status_code': response.status_code,
            'url': url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Amazon Rank Tracker Server Starting...")
    print("📡 Server running on http://localhost:5000")
    print("🔍 Test scraping with: http://localhost:5000/test/B08N5WRWNW")
    print("🛑 Press Ctrl+C to stop")
    app.run(debug=True, port=5000)