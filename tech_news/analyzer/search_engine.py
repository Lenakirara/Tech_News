from tech_news.database import db
from datetime import datetime


# função criada pois retorna uma lista de tuplas que será usadas nos searchs
def get_news_list(news):
    news_list = [(post["title"], post["url"]) for post in news]
    return news_list


# case insensitive - mongodb:
# https://stackoverflow.com/questions/1863399/mongodb-is-it-possible-to-make-a-case-insensitive-query
# https://docs.mongodb.com/manual/reference/operator/query/regex/
# https://www.mongodb.com/community/forums/t/case-insensitive-search-with-regex/120598
# Requisito 6
def search_by_title(title):
    # no teste: db.news (...)
    news = db.news.find({"title": {"$regex": title, "$options": "i"}})
    return get_news_list(news)


# Mauricio Ieiri (sala c) deu a dica de usar strptime()
# https://docs.python.org/pt-br/3/library/datetime.html?highlight=strptime
# http://www.w3big.com/pt/python/att-time-strptime.html
# https://acervolima.com/funcao-python-time-strptime/
# https://www.programiz.com/python-programming/datetime/strptime
# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        news = db.news.find({"timestamp": {"$regex": date}})
        return get_news_list(news)
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    news = db.news.find({"sources": {"$regex": source, "$options": "i"}})
    return get_news_list(news)


# Requisito 9
def search_by_category(category):
    news = db.news.find({"categories": {"$regex": category, "$options": "i"}})
    return get_news_list(news)
