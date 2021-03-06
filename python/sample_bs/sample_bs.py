import bs4
import requests
import time


def scrap_imdb():
    # pass the URL
    url = 'http://www.imdb.com/search/title'
    params = '?release_date=2010,2017&title_type=feature&user_rating=1.0,10'
    url = requests.get(url + params)
    # read the source from the URL
    read_html = url.text
    parse_result_bs(read_html)


def parse_result_bs(html_content):
    soup = bs4.BeautifulSoup(html_content, 'html.parser')

    file_name = 'results_' + time.strftime("%d_%m_%Y_%H_%M_%S") + '.txt'
    file = open(file_name, 'w')

    # passing HTML to scrape it
    table_class_results = soup.find("div", {"class": "lister-list"})
    for row in table_class_results.find_all('div', {'class': 'lister-item'}):
        contents = row.find_all('div', {"class": "lister-item-content"})
        for content in contents:
            header = content.find('h3', {'class': 'lister-item-header'})
            title = header.find('a')
            year = header.find('span', {'class': 'lister-item-year'})
            infos = content.find_all('p', {'class': 'text-muted'})
            runtime = infos[0].find('span', {'class': 'runtime'})
            genre = infos[0].find('span', {'class': 'genre'})

            rating_bar = content.find('div', {'class': 'ratings-bar'})
            rating = rating_bar.find('div', {'class': 'ratings-imdb-rating'})
            description = infos[1]

            file.write("Title: " + (title.text if title else 'n.a.'))
            file.write('\n')
            file.write("Year: " + (year.text if year else 'n.a.'))
            file.write('\n')
            file.write("Rating: " + (
                rating.get('data-value') if rating else 'n.a.'))
            file.write('\n')
            file.write("Runtime: " + (runtime.text if runtime else 'n.a.'))
            file.write('\n')
            file.write("Genre: " + (genre.text if genre else 'n.a.'))
            file.write('\n')
            file.write("Description:" + (
                description.text if description else 'n.a.'))
            file.write('\n\n')
    file.close()


scrap_imdb()

