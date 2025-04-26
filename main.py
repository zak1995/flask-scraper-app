from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from scraper import universal_scrape
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')

    try:
        html = universal_scrape(url)
        soup = BeautifulSoup(html, 'html.parser')

        products = []
        for div in soup.find_all('div'):
            title = div.find('h3') or div.find('h2') or div.find('a')
            price = div.find(string=lambda s: s and ('€' in s or '$' in s))
            img = div.find('img')
            if title and price and img:
                products.append({
                    'title': title.get_text(strip=True),
                    'price': price.strip(),
                    'image': img['src']
                })
            if len(products) >= 10:
                break

        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

