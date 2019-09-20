import logging

import scrapy
from parsedatetime import Calendar
import os

from housy.processing.file_operation import append_to_file
from housy.requirements.olx import OlxRequirements
from housy.requirements.requirements import req
from housy.requirements.otodom import OtodomRequirements
from housy.url_generator.url_generator import OlxUrlGenerator
from housy.processing.text_processing import get_processed_text, calculate_intersection, olx_convert_to_time_struct


class OlxSpider(scrapy.Spider):
    name = "olx"

    def start_requests(self):
        olx_req = OlxRequirements(req)
        url_generator = OlxUrlGenerator(olx_req)
        urls = [
            url_generator.generate_url(),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to offer pages
        offers = response.xpath('//a[@data-cy="listing-ad-title"]')
        for offer in offers:
            yield response.follow(url=offer.attrib['href'], callback=self.parse_offer)

        latest_date = response.xpath('//small//span//i[@data-icon="clock"]/../text()').getall().pop()
        olx_req = OlxRequirements(req)
        cal = Calendar()
        required_date = cal.parse(' '.join([str(olx_req.number_of_days), 'days ago']))[0]
        parsed_date = latest_date.replace('\n', '').replace('\t', '')
        latest_date_processed = olx_convert_to_time_struct(parsed_date)
        if latest_date_processed < required_date:
            return
        yield response.follow(url=response.xpath('//a[@data-cy="page-link-next"]').attrib['href'], callback=self.parse)

    def parse_offer(self, response):
        """Extracts the details of the offer to search through."""
        olx_req = OlxRequirements(req)
        li = response.xpath('//td[@class="value"]//strong//a/text()').getall()
        li_text = get_processed_text(li)
        p = response.xpath('//div[@id="textContent"]/text()').getall()
        p_text = get_processed_text(p)
        text = ' '.join([li_text, p_text])
        if calculate_intersection(text, olx_req.tags) >= olx_req.threshold:
            append_to_file(path='scrapy-data/urls.txt', response=response)

