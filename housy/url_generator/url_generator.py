import abc
import urllib.parse
import json


class AbsUrlGenerator(metaclass=abc.ABCMeta):
    """Defines an interface for creating urls for different target sites"""
    def __init__(self, requirements):
        self.requirements = requirements

    @abc.abstractmethod
    def generate_url(self):
        pass


class OtodomUrlGenerator(AbsUrlGenerator):
    def generate_url(self):
        url = '/'.join([
            'https://www.otodom.pl',
            self.requirements.renting_vs_owning,
            self.requirements.type_of_housing,
            self.requirements.city,
            '?'
        ])
        query_args = {'search[filter_float_price:from]': self.requirements.price_from,
                      'search[filter_float_price:to]': self.requirements.price_to,
                      'search[filter_enum_rooms_num][0]': self.requirements.number_of_rooms,
                      }
        return url + urllib.parse.urlencode(query_args)


class GumtreeUrlGenerator(AbsUrlGenerator):
    def generate_url(self):
        with open(file='gumtree/gumtree_region_number_dict.json') as json_file:
            gumtree_region_number = json.load(json_file)
        url = '/'.join([
            'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie',
            self.requirements.city,
            'v1c9073l32' + gumtree_region_number[self.requirements.city] + 'p1?'
        ])
        query_args = {'pr': [str(int(self.requirements.price_from)),
                             str(int(self.requirements.price_to))],
                      'nr': self.requirements.number_of_rooms,
                      }
        return url + urllib.parse.urlencode(query_args, doseq=True).replace('&pr=', ',')
