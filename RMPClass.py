import requests
import json
import math
import re
from bs4 import BeautifulSoup

class RateMyProfScraper:
        def __init__(self,schoolName):
            self.UniversityId = self.getSchoolId(schoolName)

        # scrape school id from RMP
        def getSchoolId(self,university):
            page = requests.get("https://www.ratemyprofessors.com/search.jsp?query=" + str(university))
            soup = BeautifulSoup(page.text, "html.parser")
            firstSchool = soup.find("li", { "class": "listing SCHOOL" })
            return firstSchool.find("a", href=True)['href'].split("?sid=")[1]

        # send query with school id and professor name
        def getProfessor(self,professor):
            page = requests.get("https://www.ratemyprofessors.com/filter/professor/?&page=1&queryoption=TEACHER&sid=" 
                + str(self.UniversityId) + "&query=" + str(professor))
            pageJson = json.loads(page.content)
            professors = pageJson['professors']
            self.exists = True
            return professors[0]

        def getProfessorDetail(self,professor,key):
            if professor is None:
                return "error"
            else:
                return professor[key]

        # get a professor's ratings for a specific course
        def getCourseReview(self,professor,course):
            courseReview = {}
            professorReviews = self.getProfessorReviews(professor,50,course)
            avgQuality = 0.0
            avgDifficulty = 0.0
            descriptions = {}
            i = 0
            while i < len(professorReviews):
                avgQuality += float(professorReviews[str(i)]['Quality'])
                avgDifficulty += float(professorReviews[str(i)]['Difficulty'])
                descriptions[professorReviews[str(i)]['Date']] = professorReviews[str(i)]['Description']
                i += 1
            avgQuality /= len(professorReviews)
            avgDifficulty /= len(professorReviews)
            courseReview['Professor'] = str(professor)
            courseReview['Avg Quality in Course'] = avgQuality
            courseReview['Avg Difficulty in Course'] = avgDifficulty
            courseReview['Descriptions'] = descriptions
            return courseReview

        # get all professor reviews
        def getProfessorReviews(self,professor,num,course):
            jsonReviews = {}
            count = 0
            page = requests.get("https://www.ratemyprofessors.com/ShowRatings.jsp?tid="
                + str(self.getProfessorDetail(self.getProfessor(professor), 'tid')))
            soup = BeautifulSoup(page.text, "html.parser")
            ratingsList = soup.find("ul", id="ratingsList")
            for li in ratingsList.find_all("li"):
                if not num:
                    numReviews = 50
                else:
                    numReviews = int(num)
                if len(jsonReviews) >= numReviews:
                    continue

                review = {}
                string = li.getText(separator=u'\n')
                vals = re.split('\n', string)
                newVals = vals[5::] # strip duplicate values
                if len(newVals) is not 0:
                    review['Quality'] = newVals[1]
                    review['Difficulty'] = newVals[3]
                    review['Course Number'] = newVals[5]
                    review['Rating'] = newVals[7]
                    review['Date'] = newVals[8]
                    
                    if course:
                        if review['Course Number'] != course:
                            continue
                    
                    tags = {}
                    key = ""
                    i = 0
                    lastTag = 0
                    for string in newVals:
                        if string.strip() != ":":
                            key = string
                        else:
                            tags[key] = newVals[i + 1]
                            lastTag = i + 1
                        i += 1
                    
                    if lastTag is 0:
                        review['Description'] = newVals[9]
                    else:
                        review['Description'] = newVals[lastTag + 1]

                    review['Tags'] = tags
                    jsonReviews[count] = review
                    count += 1
            return json.loads(json.dumps(jsonReviews))