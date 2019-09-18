import scrapy

from housy.requirements.gumtree import GumtreeRequirements
from housy.requirements.requirements import req
from housy.url_generator.url_generator import GumtreeUrlGenerator


class GumtreeSpider(scrapy.Spider):
    name = "gumtree"

    def start_requests(self):
        gumtree_req = GumtreeRequirements(req)
        url_generator = GumtreeUrlGenerator(gumtree_req)
        urls = [
            url_generator.generate_url(),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to offer pages
        offers = response.xpath("//a[@class='href-link tile-title-text']")
        for offer in offers:
            yield response.follow(url=offer.attrib['href'], callback=self.parse_offer)
        # follow pagination link
        tmp_1 = response.xpath("//a[@class='arrows icon-angle-right-gray icon-right-arrow']")
        tmp_2 = response.xpath("//a[@class='arrows icon-right-arrow icon-angle-right-gray']")
        next_page = tmp_1 if 'href' in tmp_1.attrib else tmp_2
        yield response.follow(
            next_page.attrib['href'],
            self.parse
        )

    def parse_offer(self, response):
        """Extracts the details of the offer to search through."""
        pass
