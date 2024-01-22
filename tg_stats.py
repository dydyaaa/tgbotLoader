import requests
from bs4 import BeautifulSoup
import re

def stat(url):
    url = 'https://tgstat.ru/channel/@' + url[13:] + '/stat'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = response.text
    flag = False
    soup = BeautifulSoup(html, 'html.parser')

    try:
        is_find = soup.find('p', class_='lead font-22').text
        if is_find == 'Канал не найден' or is_find == 'Страница не существует':
            return(is_find)
    except AttributeError:

        main_info = soup.find_all('h2', class_='text-dark')
        v1 = "Количество подписчиков: " + main_info[0].get_text(strip=True)
        v2 = re.sub(r'\D', '', main_info[6].get_text(strip=True))[::-1]
        v3 = ' '.join(v2[i:i+3] for i in range(0, len(v2), 3))
        v4 = "Публикаций: " + v3[::-1]

        b_elements = soup.find_all('b')
        variable1 = "Сегодня " + b_elements[3].get_text(strip=True)
        variable2 = "За неделю " + b_elements[4].get_text(strip=True)
        variable3 = "За месяц " + b_elements[5].get_text(strip=True)

        k = soup.find_all('div', class_='text-right')
        for i in k:
            if 'Stories' in i.text:
                flag = True
        if flag == True:
            variable4 = "Вчера: " + b_elements[22].get_text(strip=True)
            variable5 = "За неделю " + b_elements[23].get_text(strip=True)
            variable6 = "За месяц " + b_elements[24].get_text(strip=True)
        else:
            variable4 = "Вчера: " + b_elements[16].get_text(strip=True)
            variable5 = "За неделю " + b_elements[17].get_text(strip=True)
            variable6 = "За месяц " + b_elements[18].get_text(strip=True)

        return f'{v1}\n{variable1}\n{variable2}\n{variable3}\n{v4}\n{variable4}\n{variable5}\n{variable6}'
