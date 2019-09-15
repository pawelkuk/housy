import unittest
from housy.requirements.requirements import Requirements, req
from housy.url_generator.url_generator import OtodomUrlGenerator


class UrlGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.requirements = Requirements(req)
        self.requirements._requirements['price_to'] = 500000.0
        self.requirements._requirements['price_from'] = 100000.0
        self.otodom = OtodomUrlGenerator(self.requirements)

    def test_price_from_and_to_are_correct(self):
        url = self.otodom.generate_url()
        expected_url = 'https://www.otodom.pl/sprzedaz/mieszkanie/warszawa/'\
                       '?search%5Bfilter_float_price%3Afrom%5D=100000.0&search%5B'\
                       'filter_float_price%3Ato%5D=500000.0'\
                       '&search%5Bfilter_enum_rooms_num%5D%5B0%5D=2'
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
