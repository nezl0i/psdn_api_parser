import os
import json
import requests
from lxml import html
from urllib.parse import urlparse
from logs.logger import LOGGER


class SessionUrlBase(requests.Session):
    def __init__(self, url_base=None):
        super(SessionUrlBase, self).__init__()
        self.url_base = url_base

    def request(self, method, url, **kwargs):
        modified_url = self.url_base + url

        return super(SessionUrlBase, self).request(method, modified_url, **kwargs)


class HelpAPI:
    def __init__(self, url_base, href_xpath):
        self.BASE_URL = url_base
        self.HREF_XPATH = href_xpath
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                          'Safari/537.36'
        }
        self.session = SessionUrlBase(url_base=self.BASE_URL)
        self.session.headers.update(self.HEADERS)
        self.internal_url = set()

    @staticmethod
    def valid_url(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def website_links(self, start_url):

        urls = set()

        # Получаем объект страницы в виде DOM
        response = self.session.get(start_url)
        dom = html.fromstring(response.content)

        # Парсим все ссылки на странице
        start_link = dom.xpath(self.HREF_XPATH)

        # Обработка ссылок
        collection_link = [link.replace("../html/", "") for link in start_link if link.endswith('htm')]

        LOGGER.info(f'web_url: {response.url} ({len(collection_link)})')

        for url in collection_link:

            # Формируем правильный url
            href = self.BASE_URL + url

            if not self.valid_url(href):
                # Валидация url
                continue

            if href in self.internal_url:
                LOGGER.info(f'\t[-] Ссылка {href} есть в списке.')
                continue

            LOGGER.info(f"\t[+] Internal link: {href}")

            urls.add(url)
            self.internal_url.add(href)

            if os.path.isfile(f'html/{url}'):
                continue

            response = self.session.get(url)

            # Сохраняем страницу
            with open(f'html/{url}', 'w', encoding='utf8') as f:
                f.write(response.text)

        return urls

    def crawl(self, url):
        links = self.website_links(url)

        for link in links:
            self.crawl(link)


if __name__ == "__main__":

    BASE_URL = 'http://psdn.sicon.ru/html/'
    HREF_XPATH = '//a[not(contains(@class, "tocExpanded")) and not(contains(@class, "tocCollapsed"))]/@href'

    api = HelpAPI(BASE_URL, HREF_XPATH)
    api.crawl(url='1be75829-b968-495a-8958-6973e0af04d3.htm')

    with open("collect_url.json", 'w', encoding='utf8') as file:
        json.dump(list(api.internal_url), file, indent=4, ensure_ascii=False)
