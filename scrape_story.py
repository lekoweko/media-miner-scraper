from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as Soup
import time

complete_story = []
urls = []
root_url = 'https://www.mediaminer.org'


def scrape(url):
    if __name__ == "__main__":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        wd = uc.Chrome(options=options)
        time.sleep(5)
        wd.get(url)
        try:
            html_page = wd.page_source
            soup = Soup(html_page, 'html.parser')
        finally:
            wd.quit()
            if len(urls):
                get_story(soup)
            else:
                get_chapter_index(soup)


def get_chapter_index(soup):
    div = soup.find('div', class_='col-md-8')
    chapter_index = div.find('p', {'style': 'margin-left:10px;'})
    chapter_urls = chapter_index.find_all('a')
    for url in chapter_urls:
        chapter_url = url.get('href')
        urls.append(root_url + chapter_url)
    for url in urls:
        scrape(url)


def get_story(soup):
    div = soup.find(id='content')
    story_content = soup.find(id='fanfic-text')
    story_chapter = story_content.text
    complete_story.append(story_chapter)
    next_chapter = div.find(id='post-nav-next')
    if next_chapter:
        # there are summaries for each chapter
        print('now scraping next chapter')
    else:
        story_data = soup.find('div', class_='post-meta clearfix')
        metadata = {
            "Title": soup.find(id='post-title').text.split("❯")[1],
            "Rating": soup.find(id='post-rating').text,
            "Summary": story_data.find('br').next_sibling
        }
        tags = story_data.find_all('b')
        for tag in tags:
            metadata[tag.text] = tag.next_sibling.text
        metadata["Story"] = ','.join(complete_story)
        get_txt(metadata)


def get_txt(metadata):
    with open(f'{metadata["Title"]} By {metadata["By: "]}.txt', 'w') as f:
        for data in metadata:
            f.write("{}:{}\n".format(data, metadata[data]))

scrape('')

