import bs4
import time
from selenium import webdriver


def selenium_access():
    """
    Overkill, just to prove it can be done with Selenium.
    """
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir=/home/uilian/.config/google-chrome/Default/")
    driver = webdriver.Chrome(
        executable_path='/opt/selenium/chromedrive/chromedriver',
        chrome_options=options)
    url = 'http://www.imdb.com/search/title'
    params = '?release_date=2010,2017&title_type=feature&user_rating=1.0,10'
    # Optional argument, if not specified will search path.
    driver.get(url + params)
    time.sleep(1)

    # One can simulate user input instead of sending
    # all on the URL

    # parameter1 = driver.find_element_by_name('parameter1')
    # parameter1.send_keys(config_properties.parameter1)

    # parameter2 = driver.find_element_by_name('parameter2')
    # parameter2.send_keys(config_properties.parameter2)

    # link = driver.find_element_by_link_text('Submit')
    # link.click()
    # time.sleep(1)

    # button_2 = driver.find_element_by_name('button2')
    # button_2.click()

    # title = driver.find_element_by_name("title")
    # driver.execute_script(
    #     "arguments[0].value = arguments[1]",
    #     title, config_properties.title)

    page_result = driver.page_source
    driver.quit()
    parse_result_bs(page_result)


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

selenium_access()
