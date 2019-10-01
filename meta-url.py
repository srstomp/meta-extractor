import requests
import logging
from bs4 import BeautifulSoup
from flask import (
    Flask,
    request,
    jsonify,
)

app = Flask(__name__)

class MetaExtractor():

    def validateUrl(self, url):
        if url.find('https://') == -1 & url.find('http://') == -1:
            url = 'http://' + url

        return url

    def fetch(self, url):
        meta = {}
        
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        
        req = requests.get(self.validateUrl(url), headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")
        image = soup.find("meta", property="og:image")
        icon = soup.find("link", rel="apple-touch-icon")

        meta['title'] = self.getValue(title, 'content')
        meta['description'] = self.getValue(description, 'content')
        meta['image'] = self.getValue(image, 'content')

        if (meta['image']is None) | (meta['image'] == ""):
            meta['image'] = self.getValue(icon, 'href')

        return meta

    def getValue(self, object, key):
        if object is not None:
            return object.get(key)
        
        return ''
        

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/extract', methods=['GET'])
def search():
    query_parameters = request.args
    url = query_parameters.get('url', '', type=str)

    client = MetaExtractor()
    return jsonify(client.fetch(url))

if __name__ == '__main__':
    app.run(debug=True)
