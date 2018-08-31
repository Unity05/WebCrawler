from selenium import webdriver
import requests
import nltk
from bs4 import BeautifulSoup
from bs4.element import Comment
import time
import json


def split_to_sentences(content):
    sentences = nltk.sent_tokenize(content)
    return sentences


def search_for_keywords(words, keywords):
    for word in words:
        for keyword in keywords:
            if word == keyword:
                return True
    return False


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def go_through_urls(urls0):
    urls1 = []
    elems = None
    for url in urls0:
        try:
            driver.get(url)
            elems = driver.find_elements_by_xpath("//*[@href]")
            resp = requests.get(url)
            content = text_from_html(resp.text)
            sentence_dict = split_to_sentences(content)

            for sentence in sentence_dict:
                words_dict = nltk.word_tokenize(sentence)
                has_keywords = search_for_keywords(words_dict, keywords)
                if has_keywords == True:
                    important_sentences.append([sentence, url])
                    print([sentence, url])

            for elem in elems:
                urls1.append(elem.get_attribute('href'))

        except Exception:
            time.sleep(10)
            pass
    print(str(elems))
    return urls1



search_input = 'google'
keywords = ['nothing']
important_sentences = []

driver = webdriver.Chrome(r'C:\Users\Friedward\PycharmProjects\WebCrawler\chromedriver')
driver.get('https://www.google.com/')
search_field = driver.find_element_by_id('lst-ib')
search_field.send_keys(search_input)
search_field.submit()
elems = driver.find_elements_by_xpath("//*[@href]")
urls = []
for elem in elems:
    url_start = str(elem.get_attribute('href'))[ :22]
    url_sp_start = str(elem.get_attribute('href'))[ :26]
    url_li_start = str(elem.get_attribute('href'))[ :27]
    url_tl_start = str(elem.get_attribute('href'))[ :28]
    check_http = str(elem.get_attribute('href'))[ :4]
    check_https = str(elem.get_attribute('href'))[ :5]
    print(str(url_start) + ' | ' + str(url_tl_start) + ' | ' + str(url_li_start) + ' | ' + str(url_sp_start) + ' | ' + str(elem.get_attribute('href')))
    if check_http == 'http' or check_https == 'https':
        if url_start != 'https://www.google.com' \
                and url_sp_start != 'https://support.google.com' \
                and url_li_start != 'https://accounts.google.com' \
                and url_tl_start != 'https://translate.google.com':
            urls.append(elem.get_attribute('href'))

for i2 in range(5):
    urls = go_through_urls(urls)
    print(str(urls))



with open('important_content', 'w') as important_content_file:
    important_content_file.write(json.dumps(important_sentences))
