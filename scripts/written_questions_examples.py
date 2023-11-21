"""This script is used for scraping few examples from the written questions"""
# import libraries
import re
import time

from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL = 'https://www.chambredesrepresentants.ma'
WRITTEN_QUESTIONS_URL = f'{BASE_URL}/fr/questions-ecrites'
N_PAGES = 2

def get_questions_info(questions_page_url, n_page=1):
    """
    Get questions info from a questions page.
    """
    questions_page = requests.get(questions_page_url)
    if questions_page.status_code != 200:
        return None
    questions_soup = BeautifulSoup(questions_page.text, 'lxml')
    print(f'Soup created for questions page {n_page}.')
    questions_meta_info = []
    questions_divs = questions_soup('div', class_='q-block3')
    for question_div in questions_divs:
        print('Started scraping for question div.')
        question_meta_info = get_question_meta_info(question_div)
        questions_meta_info.append(question_meta_info)
        print('Question div scraped.')
        time.sleep(1)
    return questions_meta_info

def get_question_meta_info(question_div):
    """
    Get question meta info (object, link, date, author, ministry) from a question div.
    """
    div1, div2 = question_div('div', class_='q-b3-col')  
    # get subject, link and date of question from div1
    subject = div1.find('a').contents[0].strip()
    link = f"{BASE_URL}{div1.find('a').attrs['href']}"
    date = div1.findAll('div')[-1].contents[-1].strip()
    # get author and ministry of question from div2
    author = div2.find('a').text.strip()
    ministry = div2('div')[1].contents[-1].text.strip()
    # get question id, answer_date and question from question page
    question_id, answer_date, question = get_question_info(link)
    return question_id, question, author, date, answer_date, subject, ministry

def get_question_info(question_page_url):
    """
    Get question info (question_id, answer_date, question) from a question page.
    """
    question_page = requests.get(question_page_url)
    if question_page.status_code != 200:
        return None
    question_soup = BeautifulSoup(question_page.text, 'lxml')
    print('Soup created for question page.')
    _, div1, _, _, _, div3, _ = question_soup('section')[-1].find('div', class_=re.compile('q-block1')).contents
    # get question id and answer_date from div1
    question_id = div1.div.text.strip()[13:]
    answer_date = div1.findAll('div')[-1]('span')[-1].text
    # get question from div3
    question = div3('div')[-1].text.strip()[10:].strip()
    return question_id, answer_date, question

# number of pages to scrape

all_questions = []

for n in range(N_PAGES):
    if n == 0:
        questions_page_url = WRITTEN_QUESTIONS_URL
    else:
        questions_page_url = f'{WRITTEN_QUESTIONS_URL}?page={n}'
    print(f'Started scraping for page {n+1}.')
    questions_data = get_questions_info(questions_page_url, n+1)
    if questions_data is not None:
        all_questions.extend(questions_data)
    print(f'Page {n+1} scraped.')
print('All pages scraped.')

# create dataframe from questions data
questions_df = pd.DataFrame(all_questions, columns=['question_id', 'question', 'author', 'question_date', 'answer_date', 'subject', 'ministry'])

# save dataframe to csv
questions_df.to_csv('data/written_questions.csv', index=False)

# Path: scraping/example/oral_questions_examples.py