import pytest
from gumtree.url_mapper import number_to_str, extract_region


def test_returns_valic_str_repr():
    assert number_to_str(532, 6) == '000532'


def test_returns_valid_region_from_gumtree_url():
    url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/mazowieckie/v1c9073l3200001p1'
    assert extract_region(url) == 'mazowieckie'


def test_return_none_if_region_not_found():
    url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/v1c9073p1'
    assert extract_region(url) is None
