import requests
import json
import math
from bs4 import BeautifulSoup

class RateMyProfScraper:
        def __init__(self,schoolid, professor):
            self.UniversityId = schoolid
            self.Professor = self.getProfessor(professor)
            self.exists = False
            self.size = 0

        def getProfessor(self,professor):
            tempprofessorlist = []
            i = 1
            while (i <= 1):
                page = requests.get("https://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                    i) + "&queryoption=TEACHER&queryBy=teacherName&schoolID=" + str(self.UniversityId) + "&query=" + str(professor))
                temp_jsonpage = json.loads(page.content)
                temp_list = temp_jsonpage['professors']
                tempprofessorlist.extend(temp_list)
                i += 1
                self.exists = True
            print(tempprofessorlist)
            return tempprofessorlist[0]

        def PrintProfessorInfo(self):
            if self.Professor is None:
                return "error"
            else:
                return self.Professor

        def PrintProfessorDetail(self,key):
            if self.Professor is None:
                return "error"
            else:
                return self.Professor[key]

        def getProfessorReviews(self):
            reviews = []
            jsonReviews = {}
            count = 0
            page = requests.get("https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(self.PrintProfessorDetail('tid')))
            soup = BeautifulSoup(page.text, "html.parser")
            for ul in soup.find_all("ul", id="ratingsList"):
                for li in ul.find_all("li"):
                    string = li.getText(separator=u'\n')
                    stringArr = string.split("\n")
                    if stringArr is not None:
                        review = {}
                        review['courseNumber'] = stringArr[1]
                        review['rating'] = stringArr[3]
                        review['quality'] = stringArr[6]
                        review['difficulty'] = stringArr[8]
                        review['date'] = stringArr[13]
                        review['desc'] = stringArr[29]
                        jsonReviews[count] = review
                    count += 1
            return json.loads(json.dumps(reviews))
