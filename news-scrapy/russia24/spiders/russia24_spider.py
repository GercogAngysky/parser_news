from russia24.utils import clear_string
from datetime import datetime
from scrapy import Spider, Request
from pathlib import Path
from csv import reader


class Russia24Spider(Spider):

    name = "russia24-news"

    allowd_domains = ['russia24.pro']

    start_urls = ['https://russia24.pro/news']

    custom_settings = {
        'FEEDS': {
            Path(f'data/russia24_{datetime.now().strftime("%m-%d-%Y")}.csv'): {
                'format': 'csv'
                }
        },
        'LOG_FILE': 'scrapy.log',
        'LOG_LEVEL': 'INFO'
    }

    def start_requests(self):
        file = list(self.custom_settings.get('FEEDS').keys())[0]
        self._get_saved_id(file)
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        for url in response.css('.r24_article .r24_body a::attr("href")').getall():
            news_id = url.split('/')[-2]
            # if not loaded news, then request by url
            if news_id not in self.saved_id:
                yield Request(url=url, callback=self.extract_data)


    def extract_data(self, response):
        self.logger.info(response)
        yield {
            '_id': response.url.split('/')[-2],
            'url': response.url,
            'datetime': response.css('time::attr("datetime")').get(),
            'title': clear_string(response.css('.r24_left h1::text').get()),
            'source': response.css('.r24_source a::text').get(),
            'source_link': response.css('.r24_source a::attr("href")').get().strip(),
            'image': response.css('.r24_text img::attr("src")').get(),
            'text': clear_string("".join(response.xpath('//*[@class="r24_text"]//text()').getall()))
        }


    def _get_saved_id(self, file):
        with open(file, 'r') as file:
            self.saved_id = [i[0] for i in reader(file)]


    def save_page(self, response):
        page = response.url.spli('/')[-2]
        filename = f'russia24-{page}.html'
        with open(filename, 'wb') as file:
            file.write(response.body)
        self.log(f'Saved file {filename}')