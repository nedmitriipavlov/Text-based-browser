
import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore

problem_string = 'avoid noisy Unicode characters like z\u0361\u032f\u032fa\u0327\u034e\u033al\u0321\u0353\u032bg\u0339\u0332o\u0321\u033c\u0318 and byte order'



dir_path = sys.argv[-1]
stack = []

if not dir_path:
    dir_path = 'dir-for-files'

if not os.access(dir_path, os.F_OK):
    os.mkdir(dir_path)

os.chdir(dir_path)



def filename(url):
    if not url.startswith('https://'):
        return url if not url.count('.') else url[:url.index('.')]
    else:
        return url[url.index('/')+2:url.index('.')]

def valid_url(url):
    if url.count('.') >= 1:
        return True

def get_page(url):
    name = filename(url)
    working_url = url if url.startswith("https://") else f"https://{url}"
    if valid_url(url) and not os.access(name, os.F_OK):
        r = requests.get(working_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        lst = []
        for elem in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a", "ul", "ol", "li"]):
            if elem.get('href'):
                elem.string = ''.join([Fore.BLUE, elem.text, Fore.RESET])
        with open(name, 'w', encoding='utf-8') as output:
            for elem in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a", "ul", "ol", "li"]):
                lst.append(elem.text)
            output.write(' '.join(lst))
        return lst
    else:
        with open(name, 'r', encoding='utf-8') as output:
            return output.readlines()


def back_button(lst):
    if len(lst) >= 2:
        lst.pop()
        return lst.pop()

def site_var(url):
    return url.replace('.', '_')

while True:
    inp = input()
    if inp == 'exit':
        break
    if inp == 'back':
        previous_page = back_button(stack)
        if previous_page:
            print(previous_page)
        else:
            continue
    try:
        content = get_page(inp)
        for i in content:
            print(i)
        stack.append(content)
    except FileNotFoundError:
        print('Invalid URL')