import unittest
from housy.requirements.requirements import Requirements, req


class RequirementsTestCase(unittest.TestCase):
    def setUp(self):
        self.requirements = Requirements(req)

    def test_number_of_rooms_handles_None(self):
        self.requirements._requirements['number_of_rooms'] = None
        with self.assertRaises(TypeError):
            tmp = self.requirements.number_of_rooms

    def test_number_of_rooms_handles_str(self):
        self.requirements._requirements['number_of_rooms'] = 'ten'
        with self.assertRaises(ValueError):
            tmp = self.requirements.number_of_rooms

    def test_number_of_rooms_handles_negative_numbers(self):
        self.requirements._requirements['number_of_rooms'] = -10
        self.assertEqual(self.requirements.number_of_rooms, 0)

    def test_number_of_rooms_handles_positive_numbers(self):
        positive_number = 10
        self.requirements._requirements['number_of_rooms'] = positive_number
        self.assertEqual(self.requirements.number_of_rooms, positive_number)

    def test_price_from_handles_None(self):
        self.requirements._requirements['price_from'] = None
        with self.assertRaises(TypeError):
            tmp = self.requirements.price_from

    def test_price_from_handles_str(self):
        self.requirements._requirements['price_from'] = 'ten'
        with self.assertRaises(ValueError):
            tmp = self.requirements.price_from

    def test_price_from_handles_negative_numbers(self):
        self.requirements._requirements['price_from'] = -10
        self.assertEqual(self.requirements.price_from, 0)

    def test_price_from_handles_positive_numbers(self):
        positive_number = 10
        self.requirements._requirements['price_from'] = positive_number
        self.assertEqual(self.requirements.price_from, positive_number)

    def test_price_to_handles_None(self):
        self.requirements._requirements['price_to'] = None
        with self.assertRaises(TypeError):
            tmp = self.requirements.price_to

    def test_price_to_handles_str(self):
        self.requirements._requirements['price_to'] = 'ten'
        with self.assertRaises(ValueError):
            tmp = self.requirements.price_to

    def test_price_to_handles_negative_numbers(self):
        self.requirements._requirements['price_to'] = -10
        self.assertEqual(self.requirements.price_to, 0)

    def test_price_to_handles_positive_numbers(self):
        positive_number = 10
        self.requirements._requirements['price_to'] = positive_number
        self.assertEqual(self.requirements.price_to, positive_number)

    def test_city_handles_None(self):
        self.requirements._requirements['city'] = None
        with self.assertRaises(TypeError):
            tmp = self.requirements.city

    def test_city_handles_correct_str(self):
        city = 'warszawa'
        self.requirements._requirements['city'] = city
        self.assertEqual(self.requirements.city, city)

    def test_city_handles_incorrect_str(self):
        self.requirements._requirements['city'] = ' Zielona Góra   '
        self.assertEqual(self.requirements.city, 'zielona-gora')

    def test_tags_handels_incorrect_str(self):
        self.requirements._requirements['tags'] = [' Zielona Góra   ', 'Rozkładowę']
        self.assertEqual(self.requirements.tags, ['zielona gora', 'rozkladowe'])

    def test_tags_are_empty(self):
        self.requirements._requirements['tags'] = []
        self.assertEqual(self.requirements.tags, [])


if __name__ == '__main__':
    unittest.main()
