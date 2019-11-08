import requests
from bs4 import BeautifulSoup

class CinemaParser:
    def __init__(self, city = "msk"):
        self.city = city
        if self.city == 'msk':
            self.url = 'https://msk.subscity.ru/'
        else:
            self.url = 'https://spb.subscity.ru/'

    def extract_raw_content(self):
        page = requests.get(self.url)
        self.content = page.text
        return self.content


    def print_raw_content(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        print(soup.prettify())

msk_parser = CinemaParser('msk')
msk_parser.extract_raw_content()
msk_parser.print_raw_content()

