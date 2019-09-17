import scrapy
from unidecode import unidecode
from parsedatetime import Calendar
import os

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
        # TODO this yield needs to be done in a customizable way (has to work for other numbers than '9'
        if response.url[-1] != '9':
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

        def calculate_intersection(text_to_look_through, words_to_search):
            number_of_words_to_search = len(words_to_search)
            number_of_words_present = sum([1 for word in words_to_search if word in text_to_look_through])
            return number_of_words_present/number_of_words_to_search

        # Extract date of offer submission
        # We don't want an offer which is too old
        unprocessed_date = response.xpath("//div[@class='css-lh1bxu']").get()
        (_, _, unprocessed_date) = unprocessed_date.partition(':')
        (processed_date, _, _) = unprocessed_date.partition('<')
        cal = Calendar()
        offer_submission_date = cal.parse(processed_date)
        otodom_req = OtodomRequirements(req)
        required_date = cal.parse(' '.join([str(otodom_req.number_of_days), 'days ago']))
        if offer_submission_date < required_date:
            return

        li = response.xpath("//li/text()")
        li_text = get_processed_text(li)
        p = response.xpath("//p/text()")
        p_text = get_processed_text(p)
        text = ' '.join([li_text, p_text])
        threshold = 0.99  # TODO add threshold to requirements
        if calculate_intersection(text, otodom_req.tags) >= threshold:
            script_directory = os.path.dirname(os.path.realpath(__file__))
            tmp_path = os.path.realpath(script_directory).split('/')
            tmp_path = '/'.join(tmp_path[:(len(tmp_path)-1)])
            path = '/'.join([tmp_path, 'scrapy-data/urls.txt'])
            with open(file=path, mode='a') as f:
                f.write(response.url)
                f.write('\n')
