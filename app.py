from flask import Flask, request
from RMPClass import RateMyProfScraper

app = Flask(__name__, static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/professor_search', methods=['POST'])
def handle_data():
    university = RateMyProfScraper(request.form['school'])
    university.SearchProfessor(request.form['professor'])
    return university.PrintProfessorInfo()

if __name__ == '__main__':
    app.run()