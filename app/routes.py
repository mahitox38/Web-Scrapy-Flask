from flask import Flask, render_template
import json

app = Flask(__name__)

def load_data():
    with open('scraper/bookscraper/books.json', 'r', encoding='utf-8') as file:
        return json.load(file)
    

@app.route('/')
def home():
    books = load_data()
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)


