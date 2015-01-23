import requests


def fetch_from_isbndb(search_query):
    key = 'YGFPM98L'
    r = requests.get('http://isbndb.com/api/v2/json/%s/books?q=%s' %
                     (key, search_query))
    return r.json()
