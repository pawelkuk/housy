import scrapy
from parsedatetime import Calendar

from housy.requirements.gumtree import GumtreeRequirements
from housy.requirements.requirements import req
from housy.url_generator.url_generator import GumtreeUrlGenerator
from housy.processing.text_processing import extract_date


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
        offer_date = response.xpath("//div[@class='creation-date']")
        parsed_date = extract_date(offer_date[len(offer_date)-1].get())
        gumtree_req = GumtreeRequirements(req)
        cal = Calendar()
        date = cal.parse(parsed_date)
        required_date = cal.parse(' '.join([str(gumtree_req.number_of_days), 'days ago']))
        if date < required_date:
            return
        yield response.follow(next_page.attrib['href'], self.parse)

    def parse_offer(self, response):
        """Extracts the details of the offer to search through."""
        pass
