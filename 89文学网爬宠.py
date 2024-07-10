import requests
from bs4 import BeautifulSoup
import textwrap


def get_all_chapters():

    all_urls = []
    for pages in range(1, 19):
        urls = f'https://m.xbiqugew.com/chapters_46844/{pages}'
        all_urls.append({'pages': urls, 'Urls': urls})
    return all_urls


all_url = get_all_chapters()


def get_all_urls():

    lst = []
    for ur in all_url:
        r = requests.get(ur['Urls'])
        soup = BeautifulSoup(r.text, 'html.parser')
        y = soup.find_all('li')
        for li in y:
            hrefs = li.find('a')
            if not hrefs:
                continue
            lst.append((hrefs["href"], hrefs.get_text()))
    return lst


get_all_url = get_all_urls()

def get_each_page_url(url):

    lst = [url]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    body = soup.find('body', id="nr_body")
    next_page = (body.find_all('div', class_="nr_page"))[1]
    href = (next_page.find('td', class_="next").find('a', id="pb_next"))
    if '下一页' == href.get_text():
        lst.append('https://m.xbiqugew.com/book/46844/'+href['href'])
        get_each_page_url('https://m.xbiqugew.com/book/46844/' + href['href'])
    return lst


def get_chapter_content(url):

    chapter_all_page_url = get_each_page_url(url)
    lst = []
    result = []
    txt = ''
    for urls in chapter_all_page_url:
        r = requests.get(urls)
        soup = BeautifulSoup(r.text, 'html.parser')
        first_page_text = soup.find_all('div', id='nr1')[0].get_text() # 纯汉字的，无任何标签或其他东西
        lst.append(first_page_text)
    for text in lst:
        result.append(text.replace('\xa0', ''))
    for content in result:
        txt += content
    return txt


total = len(get_all_url)
index = 0
for chapter in get_all_url:
    index += 1
    print(index, total)
    url, title = chapter
    with open('%s.txt'%title, 'w') as fout:
        fout.write(textwrap.fill(get_chapter_content(url), width=70))
