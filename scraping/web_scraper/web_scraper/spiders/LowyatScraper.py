import scrapy

class LowyatScraper(scrapy.Spider):
    name = "lowyat"

    def start_requests(self):
        urls = [
            'https://forum.lowyat.net/topic/4511119'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = "lowyat-%s.html" % page

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)