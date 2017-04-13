#!/usr/bin/env python3

import sys

import requests
from bs4 import BeautifulSoup

URL = 'https://www.laas.fr/public/fr/'


def find_in_directory(name):
    req = requests.get(URL + 'searchuser', {'letter': name})
    soup = BeautifulSoup(req.content, 'html.parser')
    for guy in soup.find('div', class_='personnel').find_all('tr')[1:]:
        if 'GEPETTO' in guy.text:
            return URL + guy.find('a').attrs['href']


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(find_in_directory(sys.argv[1]))
    else:
        from greet_newcomers import get_gepetto  # noqa
        for username in get_gepetto():
            print(username.center(10), find_in_directory(username[1:]))
