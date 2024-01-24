import requests
from bs4 import BeautifulSoup
# import fake_headers
import json
import re

result = []
for page in range(10):
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    params = {
                "text": ['python', 'django', 'flask'],
                "area": ["1", "2"],
                "page": page,
            }

    response = requests.get('https://spb.hh.ru/search/vacancy', params=params, headers=headers)
    main_data = response.text
    
    if response.status_code == 200:
        main_soup = BeautifulSoup(main_data, features="lxml")

        article_list = main_soup.find_all("div", class_="vacancy-serp-item__layout")
        for item in article_list:

            title = item.find(
                'span', 
                {'data-qa': 'serp-item__title'}).text
            link = item.find("a", class_="bloko-link")["href"]
            company = item.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            city = item.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
            # print(city.split(',')[0])
            salary_all = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if salary_all:
                salary = salary_all.text
            else:
                salary = 'Не указано'    
            result.append(
                {
                    'vacancy': title,
                    'company': company,
                    'city': city.split(',')[0],
                    'salary': salary
                }
            )
print(result)
# with open('result.json', 'w', encoding="utf-8") as file:
#     json.dump(result, file, ensure_ascii=False, indent=4)