import requests
import time
from parsel import Selector


# time - sleep: https://realpython.com/python-sleep/
# https://www.programiz.com/python-programming/time/sleep
# https://docs.python.org/3/library/asyncio-task.html?highlight=timeout#timeouts
# Requests - https://realpython.com/python-requests/
# https://stackoverflow.com/questions/21965484/timeout-for-python-requests-get-entire-response
# Requisito 1
def fetch(url, timeout=3):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=timeout)
        if response.status_code != 200:
            return None
        else:
            return response.text
    except requests.Timeout:
        return None


# parsel - https://parsel.readthedocs.io/en/latest/usage.html
# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    # buscando pelo título ... .tec--card__title (tag h3) | href (link)
    news_list = [
        news
        for news in selector.css(
            "h3.tec--card__title a::attr(href)"
        ).getall()
    ]
    return news_list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page = selector.css(".tec--btn::attr(href)").get()
    if next_page:
        return next_page
    else:
        return None


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
