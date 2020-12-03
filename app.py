from flask import Flask, request, render_template
from RMPClass import RateMyProfScraper

app = Flask(__name__, static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/professor_search', methods=['POST'])
def professor_search():
    university = RateMyProfScraper(request.form['school'], request.form['professor'])
    return university.PrintProfessorInfo()

@app.route('/review_search', methods=['POST'])
def review_search():
    university = RateMyProfScraper(request.form['school'], request.form['professor'])
    return university.getProfessorReviews()

if __name__ == '__main__':
    app.run()