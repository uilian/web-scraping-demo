import bs4
import requests


def scrap_imdb():
    # pass the URL
    url = requests.get(
        "http://www.imdb.com/search/title?release_date=2010,2017&title_type=feature&user_rating=1.0,10")
    # read the source from the URL
    read_html = url.text

    # passing HTML to scrape it
    soup = bs4.BeautifulSoup(read_html, 'html.parser')

    table_class_results = soup.find("div", {"class": "lister-list"})
    for row in table_class_results.find_all('div', {'class': 'lister-item'}):
        print("\n")
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

            print("Title: " + (title.text if title else 'n.a.'))
            print("Year: " + (year.text if year else 'n.a.'))
            print("Rating: " + (rating.get('data-value') if rating else 'n.a.'))
            print("Runtime: " + (runtime.text if runtime else 'n.a.'))
            print("Genre: " + (genre.text if genre else 'n.a.'))
            #print(sub_text)
            print("Description:" + (description.text if description else 'n.a.'))


scrap_imdb()
