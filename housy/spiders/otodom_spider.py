import scrapy
from unidecode import unidecode
from parsedatetime import Calendar

from housy.requirements.requirements import req
from housy.requirements.otodom import OtodomRequirements
from housy.url_generator.url_generator import OtodomUrlGenerator


class OtodomSpider(scrapy.Spider):
    name = "otodom"

    def start_requests(self):
        otodom_req = OtodomRequirements(req)
        url_generator = OtodomUrlGenerator(otodom_req)
        urls = [
            url_generator.generate_url(),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to offer pages
        offers = response.xpath("//article")
        for offer in offers:
            yield response.follow(url=offer.attrib['data-url'], callback=self.parse_offer)
        # follow pagination link
        yield response.follow(response.xpath("//a[@data-dir='next']").attrib['href'], self.parse)

    def parse_offer(self, response):
        """Extracts the details of the offer to search through."""
        def get_processed_text(list_of_str):
            """Storing str in list to avoid memory coping."""
            tmp_list = []
            for raw_str_bit in list_of_str:
                accented_str_bit = raw_str_bit.get().strip().lower()
                str_bit = unidecode(accented_str_bit)
                tmp_list.append(str_bit)
            return ' '.join(tmp_list)

        li = response.xpath("//li/text()")
        li_text = get_processed_text(li)
        p = response.xpath("//p/text()")
        p_text = get_processed_text(p)
        text = ' '.join([li_text, p_text])
        # Extract date of offer submission
        unprocessed_date = response.xpath("//div[@class='css-lh1bxu']").get()
        (_, _, unprocessed_date) = unprocessed_date.partition(':')
        (processed_date, _, _) = unprocessed_date.partition('<')
        cal = Calendar()
        offer_submission_date = cal.parse(processed_date)
        otodom_req = OtodomRequirements(req)
