import requests
from bs4 import BeautifulSoup

class CinemaParser:
    def __init__(self, city = "msk"):
        self.city = city
        if self.city == 'msk':
            self.url = 'https://msk.subscity.ru/'
        else:
            self.url = 'https://spb.subscity.ru/'
        self.content = self.extract_raw_content()

    def extract_raw_content(self):
        page = requests.get(url = self.url)
        self.content = BeautifulSoup(page.text, 'html.parser')
        return self.content


    def print_raw_content(self):
        response = requests.get(url = self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())

    def get_films_list(self):
        films = []
        content = self.content
        div_tags = content.find_all('div', {'class', 'movie-plate'})
        for i in range(len(div_tags)):
            films.append(div_tags[i]['attr-title'])
        return films

    def get_film_nearest_session(self, film):
        film = str(film)
        film = film.lower()
        film = film.strip(' ')
        response = requests.get(url = self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tags = soup.find_all('div', {'class': 'movie-plate'})
        for i in range(len(div_tags)):
            if div_tags[i]['attr-title'].lower() == film:
                num = i
                x1 = div_tags[i].find_all('div', {'class': 'movie-plate-table'})
                y1 = x1[0].find_all('div', {'class': 'movie-plate-row'})
                day = y1[1].find_all('span', {'class': 'label label-bg label-default normal-font'})
                day = day[0].text
                if day != " сегодня":
                    print("None None")
                elif day == " сегодня":
                    name = div_tags[i]
                    link = name.find_all('a')[0]['href']
                    new_url = self.url + link
                    response_new = requests.get(url=new_url)
                    soup_new = BeautifulSoup(response_new.text, 'html.parser')
                    table_tags = soup_new.find_all('table', {'class': 'table table-bordered table-condensed table-curved table-striped table-no-inside-borders'})
                    x = table_tags[0]
                    times = x.find_all('tr', {'class': 'row-entity'})
                    tms = []
                    for i in range(len(times)):
                        q = times[i].find_all('td', {'class': 'col-sm-8 col-xs-1'})
                        x = q[0].find_all('td')
                        res = x[0]['attr-time']
                        tms.append(int(res))
                    closest_time_index = tms.index(min(tms))
                    route = times[closest_time_index].find_all('td', {'class': 'col-sm-8 col-xs-1'})
                    normal_time = route[0].find_all('a')[0]
                    v = times[closest_time_index].find_all('td', {'class': 'col-sm-4 col-xs-11'})
                    cinema = v[0].find_all('a')[0]
                    result = cinema.text, normal_time.text
                    return result



if __name__ == '__main__':
    msk_parser = CinemaParser('msk')
    spb_parser = CinemaParser('spb')
    #msk_parser.extract_raw_content()
    #msk_parser.print_raw_content()
    print(msk_parser.get_film_nearest_session('ford против Ferrari    '))
    print(spb_parser.get_film_nearest_session('Ford против Ferrari'))
