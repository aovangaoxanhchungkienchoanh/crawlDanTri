from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

st = time.time()
links,titles,description = [],[],[]


for page in range(1,2):
    url = f'https://dantri.com.vn/kinh-doanh/tai-chinh/trang-{page}.htm'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='bai-viet')
    articles = results.find_all("article", class_="article-item")

    for article in articles:
        title_element = article.find("h3", class_="article-title")
        des_element = article.find("div", class_="article-excerpt")
        location_element = article.find('a', href=True)
        links.append('https://dantri.com.vn/'+location_element['href'])
        titles.append(title_element)
        description.append(des_element)

content = []
for page_detail in links:
    page_details = requests.get(page_detail)
    soup_details = BeautifulSoup(page_details.content, 'html.parser')
    results_details = soup_details.select('.singular-container')
    for result in results_details:
        infos = result.select('h4,p')
        textline = ''
        for info in infos:
            textline += info.text
        content.append(textline)

titles = [i.text for i in titles]
description = [i.text for i in description]


file_end = pd.DataFrame(list(zip(links,titles,description,content)))
file_end.columns =['Links', 'Tiêu đề', 'Mô tả', 'Nội dung']
saveFile = file_end.to_csv('D:/Py/test/output.csv', encoding="utf-8-sig")

et = time.time()
print('Execution time:', et - st, 'seconds')