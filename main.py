'''
(c) Charles Ide, November 6 2023
This file will serve as the entrypoint for our Newsletter GPT application
'''

#from web_interface import index, process_url
from flask import Flask, render_template, request
from url_processor import get_page_content

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_url', methods=['POST'])
def process_url_route():
    if request.method == 'POST':
        url = request.form['url']
        page_content = get_page_content(url)
        return render_template('result.html', url=url, page_content=page_content)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)