"""
Extract metadata from the economist's weekly publication
"""

import datetime as dt
from soupstars import data, links, follow, exclude


current_date = dt.date.today() - dt.timedelta(days=4)
url = f'https://www.economist.com/printedition/{current_date}'
article_path_regex = "\/\d{4}\/\d{2}\/\d{2}\/"


def article_content(soup):
    return soup.article.find(attrs={'class': 'blog-post__inner'})


@exclude
def exclude(soup):
    # Don't include data from the index page
    return not soup.url.path.match(article_path_regex)


@links
def links(soup):
    # Only generate links on the seed page
    if soup.url == url:
        return [l for l in soup.links() if l.match(article_path_regex)]
    else:
        return []

@data
def date(soup):
    "The date of collection"
    return current_date


@data
def fly_title(soup):
    return soup.article.find(attrs={'class': 'flytitle-and-title__flytitle'}).text


@data
def title(soup):
    return soup.article.find(attrs={'class': 'flytitle-and-title__title'}).text


@data
def description(soup):
    return soup.article.find(attrs={'class': 'blog-post__description'}).text


@data
def section(soup):
    return soup.url.path.split('/')[1]


@data
def image(soup):
    return article_content(soup).img['src']


@data
def location(soup):
    return article_content(soup).find(attrs={'class': 'blog-post__location-created'}).text.replace('|', '').strip()


@data
def content(soup):
    body = article_content(soup)
    return [p.text for p in body.find_all('p') if p.text and 'Upgrade your inbox' not in p.text]
