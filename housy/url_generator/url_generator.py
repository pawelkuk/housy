import abc
import urllib.parse


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
