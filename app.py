#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
import sys, argparse, json

url = 'https://iprcampaign.nctu.edu.tw/quiz/quiz/'

class App:
    def __init__(self, url, cookies, answers):
        self.url = url
        self.cookies = cookies
        self.answers = answers
        self.chrome = None
        self.score = 0

    def open_browser(self):
        # open browser
        options = webdriver.ChromeOptions()
        #options.add_argument('start-maximized')
        self.chrome = webdriver.Chrome(chrome_options=options)
        # get url
        self.chrome.get(self.url)
        # add cookie
        for i in self.cookies:
            self.chrome.add_cookie(i)

    def get_url(self):
        # reopen url
        self.chrome.get(self.url)

    def get_questions(self):
        questions_xpath = '/html/body/div/div/div/form/table/tbody/tr/td[1]'
        questions = self.chrome.find_elements_by_xpath(questions_xpath)
        print('nQuestions: {}'.format(len(questions) - 1))
        if len(questions) == 0:
            print('[ERR] Invalid Cookie')
            exit(-1)

        for i in range(1,len(questions)):
            if questions[i].text in self.answers:
                ans = self.answers[questions[i].text]
            else:
                ans = randint(0, 1)
                self.answers[questions[i].text] = ans
            input_id = 'input#id_answerchoice{}_{}'.format(i-1, ans)
            radio = self.chrome.find_element_by_css_selector(input_id)
            radio.send_keys(Keys.SPACE)
            #print('{}: {}, {}'.format(i, rows[i].text, rand))

    def check_answers(self):
        html = self.chrome.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        sleep(1)
        submit_xpath = '/html/body/div/div/div/form/input[1]'
        submit_btn = self.chrome.find_element_by_xpath(submit_xpath)
        submit_btn.click()
        sleep(1)

        score_xpath = '/html/body/div/div/div/h2'
        score = self.chrome.find_element_by_xpath(score_xpath)
        score_arr = score.text.split()
        self.score = float(score_arr[-1])
        print('Score: {}'.format(self.score))

        questions_xpath = '/html/body/div/div/div/table/tbody/tr/td[1]'
        answers_xpath = '/html/body/div/div/div/table/tbody/tr/td[2]'
        questions = self.chrome.find_elements_by_xpath(questions_xpath)
        answers = self.chrome.find_elements_by_xpath(answers_xpath)
        #print('Q:{} A:{}'.format(len(questions), len(answers)))
        for i in range(0, len(questions)):
            #print('{}: {} {}'.format(i, questions[i].text, answers[i].text))
            if answers[i].text != 'True' and answers[i].text != 'False':
                #print('{}: skipped'.format(i))
                continue

            if answers[i].text == 'True':
                self.answers[questions[i].text] = 0
            else:
                self.answers[questions[i].text] = 1

    def close_browsers(self):
        self.chrome.close()

    def run(self):
        self.open_browser()
        while self.score != 100:
            self.get_url()
            self.get_questions()
            self.check_answers()
        self.close_browsers()

    def get_answers(self):
        return self.answers

def run(cookies, ans):
    app = App(url, cookies, ans)
    app.run()
    return app.get_answers()

if __name__ == '__main__':
    cookie_path = sys.path[0] + '/cookie.json'
    answer_path = sys.path[0] + '/answer.json'
    parser = argparse.ArgumentParser(
            description=
            'A script used for quiz automation.'
            )
    parser.add_argument('-c', '--cookie', default=cookie_path)
    parser.add_argument('-a', '--answer', default=answer_path)

    args = parser.parse_args()

    if not args.cookie:
        parser.print_help()
    else:
        try:
            with open(args.cookie, 'r') as f:
                cookie = json.load(f)
                cookie = cookie['cookies']
        except IOError:
            print('A valid cookie.json is required.')
            exit(-1)

        answer = {}
        try:
            with open(args.answer, 'r', encoding='utf8') as f:
                answer = json.load(f)
        except Exception:
            pass

        answer = run(cookie, answer)
        i = 1
        for k in answer:
            print('{}: {} {}'.format(i, k, answer[k]))
            i+=1

        with open(args.answer, 'w+', encoding='utf8') as f:
            json.dump(answer, f, ensure_ascii=False, indent=4)
else:
    pass
