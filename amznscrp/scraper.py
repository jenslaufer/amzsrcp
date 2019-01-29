import bottlenose
from bs4 import BeautifulSoup
import requests
import os
from os import listdir
import re
from lxml import html
import json
import urllib
import datetime
from urllib.parse import quote_plus
from . import pageelements
from . import proxy
from . import useragent


def search_api(api_key, api_secret, affiliate_id, keywords, region='DE', search_index='All', pages=1):
    amazon = bottlenose.Amazon(api_key, api_secret, affiliate_id,
                               Region=region, Parser=lambda text: BeautifulSoup(text, 'xml'))
    asins = []
    for itempage in range(1, (pages+1)):
        results = amazon.ItemSearch(
            Keywords=keywords, SearchIndex=search_index, ItemPage=str(itempage))
        for asin in results.find_all('ASIN'):
            asins.append({'asin': asin.text})

    return asins


def search(keyword, proxy_srv, user_agents):
    s = requests.session()
    headers = {
        'User-Agent': user_agents.get(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    proxies = proxy_srv.get()
    url = "https://www.amazon.de/s/ref=nb_sb_noss_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords={}".format(
        quote_plus(keyword))
    try:
        result = s.get(url, headers=headers, proxies=proxies)

        return {"keyword": keyword, "content": result.content}
    except Exception as e:
        print(e)


def extract_features(asin, content):
    doc = html.fromstring(content)

    data = {
        'asin': asin,
        'image': pageelements.get_image(doc),
        'name': pageelements.get_name(doc),
        'price': pageelements.get_price_val(doc),
        'currency': pageelements.get_currency(doc),
        'reviews_count': pageelements.get_reviews_count(doc),
        'reviews': pageelements.get_reviews(doc),
        'category_path': pageelements.get_category(doc),
        'category': pageelements.get_top_category(doc),
        'bsr': pageelements.get_bsr(doc),
        'dim_x': pageelements.get_dim_x(doc),
        'dim_y': pageelements.get_dim_y(doc),
        'dim_z': pageelements.get_dim_z(doc),
        'dim_unit': pageelements.get_dim_unit(doc),
        'weight': pageelements.get_weight_val(doc),
        'weight_unit': pageelements.get_weight_unit(doc)
    }

    return data


def fetch(asin, proxy_srv, user_agents, region='DE'):
    if region == 'DE':
        base_url = "http://www.amazon.de"

    url = "{}/dp/{}".format(base_url, asin)
    print("Downloading: "+url)
    headers = {
        'User-Agent': user_agents.get()}
    proxies = proxy_srv.get()
    try:
        res = requests.get(url, headers=headers, proxies=proxies)
        return {"asin": asin, "content": res.text}
    except Exception as e:
        print(e)
