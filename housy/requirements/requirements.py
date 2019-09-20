import unidecode

# Add here all requirements for your house search
req = {
    'number_of_rooms': 2,               # should be non-negative integer
    'price_from': 1e5,                  # should be non-negative float
    'price_to': 5e5,                    # should be non-negative float
    'type_of_housing': 'mieszkanie',    # available are: mieszkanie, dom, pokoj, dzialka, garaz
    'renting_vs_owning': 'sprzedaz',    # available are: sprzedaz, wynajem
    'city': 'warszawa',                 # lowercase name of the city ascii chars (with a dash instead of spaces)
    'tags': [                           # words the offer has to contain
        'oddziel',
        'rozkl',
    ],
    'threshold': 0.1,                  # the fraction of the words (in tags) which has to appear in the offer
    'number_of_days': 1,                # number of days the offer stands on the website
}


class Requirements:
    """Processes the requirements common to all pages one want to scrap.

    To get new requirement:
    - add key-value pair to requirements
    - add property
    - add tests for value validation

    Properties for requirements specific to just a particular site should
    be defined in subclasses.

    """

    def __init__(self, requirements):
        self._requirements = requirements  # set it to conf

    def _get_property(self, property_name):
        if property_name not in self._requirements.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._requirements[property_name]

    @property
    def number_of_rooms(self):
        try:
            number_of_rooms = int(self._get_property('number_of_rooms'))
        except ValueError:
            raise ValueError('number_of_rooms could no be converted to int')
        except TypeError:
            raise TypeError('number_of_rooms can not be None')
        return number_of_rooms if number_of_rooms > 0 else 0

    @property
    def price_from(self):
        try:
            price_from = float(self._get_property('price_from'))
        except ValueError:
            raise ValueError('price_from could no be converted to float')
        except TypeError:
            raise TypeError('price_from can not be None')
        return price_from if price_from > 0 else 0

    @property
    def price_to(self):
        try:
            price_to = float(self._get_property('price_to'))
        except ValueError:
            raise ValueError('price_to could no be converted to float')
        except TypeError:
            raise TypeError('price_to can not be None')
        return price_to if price_to > 0 else 0

    @property
    def type_of_housing(self):
        type_of_housing = self._get_property('type_of_housing')
        if type_of_housing is None:
            raise TypeError('type_of_housing can not be None')
        return str(type_of_housing)

    @property
    def renting_vs_owning(self):
        renting_vs_owning = self._get_property('renting_vs_owning')
        if renting_vs_owning is None:
            raise TypeError('renting_vs_owning can not be None')
        return str(renting_vs_owning)

    @property
    def city(self):
        city = self._get_property('city')
        if city is None:
            raise TypeError('city can not be None')
        accented_city = str(city).strip().replace(' ', '-').lower()
        return unidecode.unidecode(accented_city)

    @property
    def tags(self):
        tags = self._get_property('tags')
        if tags is None:
            raise TypeError('tags can not be None')
        if len(tags) > 0:
            accented_tags = [str(tag).strip().lower() for tag in tags]
            return [unidecode.unidecode(accented_tag) for accented_tag in accented_tags]
        return []

    @property
    def number_of_days(self):
        try:
            number_of_days = int(self._get_property('number_of_days'))
        except ValueError:
            raise ValueError('number_of_days could no be converted to int')
        except TypeError:
            raise TypeError('number_of_days can not be None')
        return number_of_days if number_of_days > 0 else 0

    @property
    def threshold(self):
        try:
            threshold = float(self._get_property('threshold'))
        except ValueError:
            raise ValueError('threshold could no be converted to float')
        except TypeError:
            raise TypeError('threshold can not be None')
        return min(1.0, threshold) if threshold > 0 else 0
