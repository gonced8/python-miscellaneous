import requests
from bs4 import BeautifulSoup

PARSE = True

URL = "https://fenix.tecnico.ulisboa.pt/cursos/meaer/paginas-de-disciplinas"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

content = soup.find("div", id="content-block")
semesters = content.find_all("div", class_="row")

data = []

for semester in semesters:
    s = semester.find("h3").find(text=True).strip()
    if PARSE:
        s = int(s[0])

    years = semester.find_all("div", class_="col-sm-12")

    for year in years:
        y = year.find("h4").text.strip()
        if PARSE:
            y = int(y[-1])

        courses = year.find_all("li")

        for course in courses:
            n = course.text.strip()
            u = course.find('a')['href']
            data.append({"name": n, "year": y, "semester": s, "url": u})

for elem in data:
    print(elem)
