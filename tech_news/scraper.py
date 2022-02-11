import requests
import time
from parsel import Selector
from tech_news.database import create_news


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


# tive que mudar css de .tec--author__info__link::text
# para .z--font-bold *::text (as paginas de url nos teste tem esse mesmo css)
# O * irá visitar todas as tags internas
def get_writer(selector):
    writer = selector.css(".z--font-bold *::text").get()
    if writer:
        # retirando os espaços em branco no inicio e no final - strip()
        return writer.strip()
    else:
        return None


def get_shares_count(selector):
    shares_count = selector.css(".tec--toolbar__item::text").get()
    # int() - para apresentar um numero inteiro
    # split - separar as strs e buscar o primeiro elemento
    if shares_count:
        return int(shares_count.split()[0])
    else:
        return 0


def get_comments_count(selector):
    comments_count = selector.css("#js-comments-btn::attr(data-count)").get()
    # puxando pelo atributo: data-count (css)
    # int() - para apresentar um numero inteiro
    if comments_count:
        return int(comments_count)
    else:
        return 0


# https://www.pythonprogressivo.net/2018/10/Unir-Separar-Strings-join-split-Tutorial-Python.html
def get_summary(selector):
    summary = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()
    # join para juntar o texto:['O CEO da ', 'Tesla', ', ', 'Elon Musk'...]
    paragraph = "".join(summary)
    return paragraph


# strip() | list Comprehension:
# https://stackoverflow.com/questions/28534125/list-comprehension-elegantly-strip-and-remove-empty-elements-in-list
def get_sources(selector):
    # .z--mb-16 div a::text - css usado para pegar a fonte correta
    # usando css -> .tec--badge::text estava buscando tanto source qto category
    sources = [
        source.strip()
        for source in selector.css(".z--mb-16 div a::text").getall()
    ]
    return sources


def get_categories(selector):
    categories = [
        category.strip()
        for category in selector.css(".tec--badge--primary ::text").getall()
    ]
    return categories


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestamp = selector.css("#js-article-date::attr(datetime)").get()
    writer = get_writer(selector)
    shares_count = get_shares_count(selector)
    comments_count = get_comments_count(selector)
    summary = get_summary(selector)
    sources = get_sources(selector)
    categories = get_categories(selector)

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


# Requisito 5
def get_tech_news(amount):
    URL_BASE = fetch("https://www.tecmundo.com.br/novidades")
    last_news_urls = scrape_novidades(URL_BASE)

    # no teste: amount", [20, 30, 40]
    while len(last_news_urls) < amount:
        next_page_link = scrape_next_page_link(URL_BASE)
        html_page = fetch(next_page_link)
        news_urls = scrape_novidades(html_page)
        last_news_urls.extend(news_urls)

    news_list = []
    # buscaremos cada 'url_link' no 'last_news_urls'
    # 'url_link' que serão iterados
    # https://www.digitalocean.com/community/tutorials/how-to-index-and-slice-strings-in-python-3-pt
    for url_link in last_news_urls[:amount]:
        html_news = fetch(url_link)
        news_list.append(scrape_noticia(html_news))

    create_news(news_list)

    return news_list

# extend() X append()
# https://www.geeksforgeeks.org/append-extend-python/
# https://pt.stackoverflow.com/questions/170741/num-list-qual-%C3%A9-a-diferen%C3%A7a-entre-append-e-extend
