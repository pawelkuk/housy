# Add here all requirements for your house search
req = {
    'number_of_rooms': 2,  # should be non-negative integer
    'price_from': 1e5,  # should be non-negative float
    'price_to': 5e5,  # should be non-negative float
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
