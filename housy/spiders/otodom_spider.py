import logging

import scrapy
from parsedatetime import Calendar
import os

from housy.processing.file_operation import append_to_file
from housy.requirements.requirements import req
from housy.requirements.otodom import OtodomRequirements
from housy.url_generator.url_generator import OtodomUrlGenerator
from housy.processing.text_processing import get_processed_text, calculate_intersection


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
        li = response.xpath("//li/text()").getall()
        li_text = get_processed_text(li)
        p = response.xpath("//p/text()").getall()
        p_text = get_processed_text(p)
        text = ' '.join([li_text, p_text])
        if calculate_intersection(text, otodom_req.tags) >= otodom_req.threshold:
            append_to_file(path='scrapy-data/urls.txt', response=response)

