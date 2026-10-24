import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.ausbildung.de/berufe/kaufmann-fuer-digitalisierungsmanagement/bewertungen/'

systemintegration = []
suggestion_col = []
opinion_col = []
company_col = []
ausbildung_place_col = []
ausbildung_begin_col = []
salary_col = []
study_condition_col = []
beruf = []

for page in range(1,4):
    response = requests.get(URL + f"?page={str(page)}")

    # ...code == 200 means the request went successful
    if response.status_code == 200:
        print('Page fetched Successfully.')
    else:
        print('Fetching failed')

    soup = BeautifulSoup(response.content, 'html.parser')
    
    empfehlung = []
    suggestions = soup.find_all('img', class_="ReviewCard-module__WnRNPG__recommendationAvatar")
    for suggestion in suggestions:
        get_suggestion = suggestion.find_next()
        if get_suggestion.name == 'p':
            empfehlung.append(get_suggestion.text)
        else:
            empfehlung.append('Unknown')

    opinions = []
    opinion_container = soup.find_all('section', class_='ReviewCard-module__WnRNPG__comments')
    for container in opinion_container:
        opinions.append(container.text)
        
    company_container = soup.find_all('header', class_='ReviewCard-module__WnRNPG__apprenticeshipCompany')
    companies = []
    for container in company_container:
        get_company = container.find('h3')
        if get_company is None: 
            companies.append('Unknown')
        else:
            companies.append(get_company.text)
             

    ausbildung_info = soup.find_all('span', class_='ReviewCard-module__WnRNPG__apprenticeshipDetailValue')
    infos = []
    for p in ausbildung_info:
        infos.append(p.text)

    ausbildung_place = infos[::3]

    ausbildung_begin = infos[1::3]


    salary = soup.find_all('dl', class_='ReviewCard-module__WnRNPG__apprenticeshipSalaryDl')
    salaries = []
    for s in salary:
        if '€' in s.text:
            salaries.append(s.text)
        else:
            salaries.append('None')

    study_conditions = []
    get_container = soup.find_all('div', class_="ReviewCard-module__WnRNPG__apprenticeshipMain")

    for container in get_container:
        for tag in container:
            tags = []
            tags.append(tag.name)
        if 'div' in tags:
            get_condition = container.contents[-1].find_next()
            study_conditions.append(get_condition.text)
        else:
            study_conditions.append('Unknown')


    suggestion_col.extend(empfehlung)
    opinion_col.extend(opinions)
    company_col.extend(companies)
    ausbildung_place_col.extend(ausbildung_place)
    ausbildung_begin_col.extend(ausbildung_begin)
    salary_col.extend(salaries)
    study_condition_col.extend(study_conditions)

    for i in range(len(companies)):
        beruf.append('kaufmann(frau) für digitalisierungsmanagement')


df = pd.DataFrame({
    'suggestion': suggestion_col,
    'opinion': opinion_col,
    'company': company_col,
    'ausbildung place': ausbildung_place_col,
    'ausbildung begin': ausbildung_begin_col,
    'salary': salary_col,
    'study condition': study_condition_col,
    'beruf': beruf
})

df.to_csv('kaufmann(frau) für digitalisierungsmanagement.csv', index=False)

