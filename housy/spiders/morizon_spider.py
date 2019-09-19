import logging

import scrapy
from parsedatetime import Calendar
import os

from housy.processing.file_operation import append_to_file
from housy.requirements.morizon import MorizonRequirements
from housy.requirements.requirements import req
from housy.requirements.otodom import OtodomRequirements
from housy.url_generator.url_generator import OtodomUrlGenerator, MorizonUrlGenerator
from housy.processing.text_processing import get_processed_text, calculate_intersection, extract_from_tag, \
    morizon_convert_to_time_struct


class MorizonSpider(scrapy.Spider):
    name = "morizon"

    def start_requests(self):
        morizon_req = MorizonRequirements(req)
        url_generator = MorizonUrlGenerator(morizon_req)
        urls = [
            url_generator.generate_url(),
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to offer pages
        offers = response.xpath("//a[@class='property_link property-url']")
        for offer in offers:
            yield response.follow(url=offer.attrib['href'], callback=self.parse_offer)

        latest_date = response.xpath("//span[@class='single-result__category single-result__category--date']")\
                              .getall()\
                              .pop()
        if 'strong' not in latest_date:
            morizon_req = MorizonRequirements(req)
            cal = Calendar()
            required_date = cal.parse(' '.join([str(morizon_req.number_of_days), 'days ago']))
            parsed_date = extract_from_tag(latest_date)
            latest_date_processed = morizon_convert_to_time_struct(parsed_date)
            if latest_date_processed < required_date:
                return
        yield response.follow(
            url=response.xpath("//a[@class='mz-pagination-number__btn mz-pagination-number__btn--next']")
                        .pop()
                        .attrib['href'],
            callback=self.parse)

    def parse_offer(self, response):
        """Extracts the details of the offer to search through."""
        morizon_req = MorizonRequirements(req)
        td = response.xpath('//section[@class="propertyDetails"]//td/text()').getall()
        td_text = get_processed_text(td)
        p = response.xpath('//section[@class="propertyDetails"]//p/text()').getall()
        p_text = get_processed_text(p)
        text = ' '.join([td_text, p_text])
        if calculate_intersection(text, morizon_req.tags) >= morizon_req.threshold:
            append_to_file(path='scrapy-data/urls.txt', response=response)
