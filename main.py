import requests
from bs4 import BeautifulSoup as BS
from bs4 import Comment
import csv
import os
from list_of_games import YEAR

URL = 'https://www.baseball-reference.com/boxes/ANA/ANA202104010.shtml'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}


def parse_page(html):
    team_n = 0
    with open(f'list_of_games_{YEAR}.csv', 'r', encoding='utf-8') as html_file:
        list_of_links = csv.reader(html_file, delimiter=';')
        links = [row[0] for row in list_of_links]

    team_stat = {'Away_team': '', 'Home_team': '', 'date': '', 'link': links[int(f'{html.split("-")[0]}') - 1],
                 'away_AB': '',
                 'away_R': '', 'away_H': '', 'away_RBI': '', 'away_BB': '', 'away_SO': '', 'away_PA': '', 'away_BA': '',
                 'away_OBP': '', 'away_SLG': '', 'away_OPS': '', 'away_str': '', 'away_p_H': '', 'away_p_R': '',
                 'away_p_ER': '', 'away_pBB': '', 'away_p_SO': '', 'away_p_ERA': '', 'home_AB': '', 'home_R': '',
                 'home_H': '', 'home_RBI': '', 'home_BB': '', 'home_SO': '', 'home_PA': '', 'home_BA': '',
                 'home_OBP': '', 'home_SLG': '', 'home_OPS': '', 'home_str': '', 'home_p_H': '', 'home_p_R': '',
                 'home_p_ER': '', 'home_pBB': '', 'home_p_SO': '', 'home_p_ERA': '', 'home_win': ''}

    with open(f'html_{YEAR}\\{html}', encoding='utf-8', newline='') as file:
        read_file = file.read()
        bs = BS(read_file, 'lxml')
        tables = bs.find_all(string=lambda text: isinstance(text, Comment))
        teams = bs.find('table', class_='linescore').find_all('a', href=lambda x: "/teams/" in x)
        team_stat['Away_team'] = teams[0].text
        team_stat['Home_team'] = teams[1].text
        # team_stat['date']= ', '.join(bs.find('div',class_='scorebox_meta').div.get_text().strip().split(', ')[::-1][:2][::-1]).replace('  ', ' ')
        team_stat['date'] = ', '.join(bs.find('h1').text.strip().split(', ')[::-1][:2][::-1]).replace('  ', ' ')
        for table in tables:
            commented_table = BS(table.extract(), 'lxml')
            if commented_table.find_all('div', {'class': 'table_container'}) is not None and commented_table.find(
                    text='Team Totals') is not None:
                for z in commented_table.find_all('div', {'class': 'table_container'}):
                    team_n += 1
                    if team_n == 1:
                        """"Away team"""
                        team_stat['away_AB'] = z.find('tfoot').find('td', {'data-stat': 'AB'}).text
                        team_stat['away_R'] = z.find('tfoot').find('td', {'data-stat': 'R'}).text
                        team_stat['away_H'] = z.find('tfoot').find('td', {'data-stat': 'H'}).text
                        team_stat['away_RBI'] = z.find('tfoot').find('td', {'data-stat': 'RBI'}).text
                        team_stat['away_BB'] = z.find('tfoot').find('td', {'data-stat': 'BB'}).text
                        team_stat['away_SO'] = z.find('tfoot').find('td', {'data-stat': 'SO'}).text
                        team_stat['away_PA'] = z.find('tfoot').find('td', {'data-stat': 'PA'}).text
                        team_stat['away_BA'] = z.find('tfoot').find('td', {'data-stat': 'batting_avg'}).text
                        team_stat['away_OBP'] = z.find('tfoot').find('td', {'data-stat': 'onbase_perc'}).text
                        team_stat['away_SLG'] = z.find('tfoot').find('td', {'data-stat': 'slugging_perc'}).text
                        team_stat['away_OPS'] = z.find('tfoot').find('td', {'data-stat': 'onbase_plus_slugging'}).text
                        team_stat['away_p_H'] = z.find('tfoot').find('td', {'data-stat': 'pitches'}).text
                        team_stat['away_str'] = z.find('tfoot').find('td', {'data-stat': 'strikes_total'}).text

                    if team_n == 2:
                        """"Home team"""
                        team_stat['home_AB'] = z.find('tfoot').find('td', {'data-stat': 'AB'}).text
                        team_stat['home_R'] = z.find('tfoot').find('td', {'data-stat': 'R'}).text
                        team_stat['home_H'] = z.find('tfoot').find('td', {'data-stat': 'H'}).text
                        team_stat['home_RBI'] = z.find('tfoot').find('td', {'data-stat': 'RBI'}).text
                        team_stat['home_BB'] = z.find('tfoot').find('td', {'data-stat': 'BB'}).text
                        team_stat['home_SO'] = z.find('tfoot').find('td', {'data-stat': 'SO'}).text
                        team_stat['home_PA'] = z.find('tfoot').find('td', {'data-stat': 'PA'}).text
                        team_stat['home_BA'] = z.find('tfoot').find('td', {'data-stat': 'batting_avg'}).text
                        team_stat['home_OBP'] = z.find('tfoot').find('td', {'data-stat': 'onbase_perc'}).text
                        team_stat['home_SLG'] = z.find('tfoot').find('td', {'data-stat': 'slugging_perc'}).text
                        team_stat['home_OPS'] = z.find('tfoot').find('td', {'data-stat': 'onbase_plus_slugging'}).text
                        team_stat['home_p_H'] = z.find('tfoot').find('td', {'data-stat': 'pitches'}).text
                        team_stat['home_str'] = z.find('tfoot').find('td', {'data-stat': 'strikes_total'}).text
                    if team_n == 3:
                        list_3 = list(z.find('th', text="Team Totals").next_siblings)
                        team_stat['away_p_H'] = list_3[1].text
                        team_stat['away_p_R'] = list_3[2].text
                        team_stat['away_p_ER'] = list_3[3].text
                        team_stat['away_pBB'] = list_3[4].text
                        team_stat['away_p_SO'] = list_3[5].text
                        team_stat['away_p_ERA'] = list_3[7].text
                    if team_n == 4:
                        list_4 = list(z.find('th', text="Team Totals").next_siblings)
                        team_stat['home_p_H'] = list_4[1].text
                        team_stat['home_p_R'] = list_4[2].text
                        team_stat['home_p_ER'] = list_4[3].text
                        team_stat['home_pBB'] = list_4[4].text
                        team_stat['home_p_SO'] = list_4[5].text
                        team_stat['home_p_ERA'] = list_4[7].text

    if int(team_stat['home_R']) > int(team_stat['away_R']):
        team_stat['home_win'] = 'TRUE'
    else:
        team_stat['home_win'] = "FALSE"
    return team_stat


def saving_results(name_of_csv=f'output_{YEAR}.csv'):
    for n, html_file in enumerate(os.listdir(f'html_{YEAR}/')):
        print(f"parse {n} of {len(os.listdir(f'html_{YEAR}/'))}")
        data = parse_page(html_file)
        with open(f'{name_of_csv}', 'a', encoding='utf-8', newline='') as csvfile:
            fieldnames = [i for i, x in data.items()]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            if n == 0:
                writer.writeheader()
            writer.writerow(data)


def start():
    import list_of_games
    list_of_games.YEAR
    question = input('Are you already saved html pages? (y/n)')
    if question == 'y':
        saving_results()
    elif question == 'n':
        question_two = input('Do you have list of html pages (y/n)')
        if question_two == 'y':
            list_of_games.saving_games_to_html()
            saving_results()
        elif question == 'n':
            list_of_games.request_and_save_to_csv()
            list_of_games.saving_games_to_html()
            saving_results()
        else:
            print('Incorrect typing. pls answer only "y" or "n"')
            start()
    else:
        print('Incorrect typing. pls answer only "y" or "n"')
        start()


if __name__ == '__main__':
    start()
    print(f'Done. Data is saved to output_{YEAR}.csv')
