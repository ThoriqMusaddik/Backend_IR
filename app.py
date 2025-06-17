from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os  # ← Tambahkan ini untuk baca PORT dari environment

app = Flask(__name__)
CORS(app)

def scrape_kompas(keyword, start_date, end_date):
    url = f"https://www.kompas.tv/search/{keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
     
    data = []
    articles = soup.select('.search__item')
    
    for article in articles:
        try:
            title = article.select_one('.search__title').get_text(strip=True)
            link = article.select_one('a')['href']
            date_str = article.select_one('.search__date').get_text(strip=True)
            date = datetime.strptime(date_str, "%d %B %Y")

            if start_date <= date <= end_date:
                data.append({
                    'title': title,
                    'date': date.strftime('%d %B %Y'),
                    'link': link
                })
        except Exception as e:
            print("Error parsing article:", e)
            continue

    return data

@app.route('/scrape', methods=['GET'])
def scrape():
    keyword = request.args.get('keyword')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    data = scrape_kompas(keyword, start_date, end_date)
    return jsonify(data)

# ✅ Inilah bagian yang kamu minta untuk ditambahkan:
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway akan memberi PORT secara otomatis
    app.run(host='0.0.0.0', port=port)