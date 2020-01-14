import requests
from bs4 import BeautifulSoup

def get_latest_movie():
    '''searches for profile on letterbox and takes last watched film and and returns its name'''
    watchlist_selector = "#recent-activity > ul > li:nth-child(1) > div"
    score_selector = "#recent-activity > ul > li:nth-child(1) > p > span"

    url = 'https://letterboxd.com/sjmignot/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    film_name = soup.select_one(watchlist_selector)['data-film-name']
    score = soup.select_one(score_selector)
    print(score.text)
    print(film_name)
    return film_name, score.text

def get_latest_book():
    pass

def get_latest_top_artist():
    pass

if __name__ == '__main__':
    get_latest_movie()
