from tech_news.database import db


# case insensitive - mongodb:
# https://stackoverflow.com/questions/1863399/mongodb-is-it-possible-to-make-a-case-insensitive-query
# https://docs.mongodb.com/manual/reference/operator/query/regex/
# https://www.mongodb.com/community/forums/t/case-insensitive-search-with-regex/120598
# Requisito 6
def search_by_title(title):
    # no teste: db.news (...)
    news = db.news.find({"title": {"$regex": title, "$options": "i"}})
    news_list = [(post["title"], post["url"]) for post in news]
    return news_list


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
