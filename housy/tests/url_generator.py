import unittest
from housy.requirements.requirements import Requirements, req
from housy.url_generator.url_generator import OtodomUrlGenerator, GumtreeUrlGenerator, MorizonUrlGenerator


class UrlGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.requirements = Requirements(req)
        self.requirements._requirements['price_to'] = 500000.0
        self.requirements._requirements['price_from'] = 100000.0
        self.otodom = OtodomUrlGenerator(self.requirements)
        self.gumtree = GumtreeUrlGenerator(self.requirements)
        self.morizon = MorizonUrlGenerator(self.requirements)

    def test_otodom_url_with_correct_reqs_is_generated(self):
        url = self.otodom.generate_url()
        expected_url = 'https://www.otodom.pl/sprzedaz/mieszkanie/warszawa/'\
                       '?search%5Bfilter_float_price%3Afrom%5D=100000.0&search%5B'\
                       'filter_float_price%3Ato%5D=500000.0'\
                       '&search%5Bfilter_enum_rooms_num%5D%5B0%5D=2'
        self.assertEqual(url, expected_url)

    def test_gumtree_url_with_correct_reqs_is_generated(self):
        url = self.gumtree.generate_url()
        expected_url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/'\
                       'warszawa/v1c9073l3200008p1?pr=100000,500000&nr=2'
        self.assertEqual(url, expected_url)

    def test_morizon_url_with_correct_reqs_is_generated(self):
        url = self.morizon.generate_url()
        expected_url = 'https://www.morizon.pl/mieszkania/najnowsze/warszawa/?' \
                       'ps%5Bprice_from%5D=100000&' \
                       'ps%5Bprice_to%5D=500000&' \
                       'ps%5Bnumber_of_rooms_from%5D=2&' \
                       'ps%5Bnumber_of_rooms_to%5D=2'
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
