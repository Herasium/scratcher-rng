from proxy import ProxyScraper
import random
from fp.fp import FreeProxy
import requests

country_codes = [
    "US", "CA",  # North America
    "GB", "DE", "FR", "IT", "ES",  # Europe
    "JP", "CN", "KR"  # East Asia
]

proxy_list = []

for country in country_codes:
    try:
        proxy = FreeProxy(country_id=[country]).get()

        a = requests.get("https://api.myip.com",proxies={"https":proxy})
        proxy_list.append(proxy)
        print("Fetched country",country)
    except Exception as e:
        print(e)
        print("Failed country",country)
print(a.status_code,a.text)