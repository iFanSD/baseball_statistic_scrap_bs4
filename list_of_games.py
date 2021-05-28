import requests
from bs4 import BeautifulSoup as BS
import csv
import lxml
import os

URL = 'https://www.baseball-reference.com/leagues/MLB/2021-schedule.shtml'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}
YEAR = int(input('Input year of the season: '))


def request(url):
    """Making request"""
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.text
    elif r.status_code==404:
        return f'Incorect year or data doesnt exist at url {url}'
    else:
        return f'somthing goes wrong at {url}'


def saving_html(page, name):
    """Saving to html file"""
    with open(f'{name}.html', 'w', encoding='utf-8') as html_file:
        html_file.write(page)


# saving_html(request(URL),'list_of_games')
def request_and_save_to_csv(name_of_csv=f'list_of_games_{YEAR}.csv', year=YEAR):
    """Request and save to csv all links to games
    :param name_of_csv: Name of csv file
    """
    print(f'Start saving list of matches in season {year}')
    html_requested = request(f'https://www.baseball-reference.com/leagues/MLB/{year}-schedule.shtml')
    saving_html(html_requested,f'list_of_games_{year}')
    bs = BS(html_requested, 'lxml')
    links = bs.find_all('p', class_='game')
    for i in links:
        if i.find('a', text='Boxscore'):
            with open(f'{name_of_csv}', 'a', encoding='utf-8', newline='') as csvfile:
                file = csv.writer(csvfile, delimiter=';', )
                file.writerow([f"https://www.baseball-reference.com{i.find('a', text='Boxscore')['href']}"] + [
                    i.find_all('a')[0].text.replace(' ', '_').replace('.', '')] + [
                                  i.find_all('a')[1].text.replace(' ', '_').replace('.', '')])


def saving_games_to_html(name_of_csv=f'list_of_games_{YEAR}.csv'):
    """Saving to html file"""
    with open(f'{name_of_csv}', 'r', newline='', encoding='utf-8') as list_of_html:
        list_of_links = csv.reader(list_of_html, delimiter=';')
        for n, row in enumerate(list_of_links):
            if os.path.exists(f"html_{YEAR}/"):
                pass
            else:
                os.mkdir(f'html_{YEAR}')
            with open(f"html_{YEAR}/{n + 1}-{row[1]}-{row[2]}.html", 'wt', encoding='utf-8') as game_file:
                game_file.write(request(row[0]))
                print(f"html/{n + 1}-{row[1]}-{row[2]}.html saved")
