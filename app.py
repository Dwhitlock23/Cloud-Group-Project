from flask import Flask, request, render_template
from RMPClass import RateMyProfScraper

app = Flask(__name__, static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/professor_search', methods=['GET'])
def professor_search():
    try:
        university = RateMyProfScraper(request.args['school'])
        return university.getProfessor(request.args['professor'])
    except:
        return app.send_static_file('error.html')

@app.route('/review_search', methods=['GET'])
def review_search():
    try:
        university = RateMyProfScraper(request.args['school'])
        response = university.getProfessorReviews(request.args['professor'],
            request.args['numReviews'], request.args['courseNumber'])
        return response
    except:
        return app.send_static_file('error.html')

@app.route('/schedule_search', methods=['POST'])
def schedule_search():
    try:
        university = RateMyProfScraper(request.form['school'])
        data = {}
        numCourses = len(request.form) / 3
        i = 0
        while i < numCourses:
            professor = None
            course = None
            for k in request.form.keys():
                if k.endswith(str(i)):
                    if k.startswith("professor"):
                        professor = request.form[k]
                    else:
                        course = request.form[k]
            data[course] = university.getCourseReview(professor, course)
            i += 1
        return data
    except:
        return app.send_static_file('error.html')

if __name__ == '__main__':
    app.run()