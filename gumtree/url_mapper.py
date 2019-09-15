import requests
import json
import os
from tqdm import tqdm


def number_to_str(num, length):
    """Helper function for generating urls."""
    str_number = str(int(num))
    n_of_zeros = length - len(str_number)
    return ''.join([n_of_zeros*'0', str_number])


def extract_region(url):
    """Given a gumtree url from the real estate section function extracts region of properties"""
    url_list = url.split('/')
    if len(url_list) != 6:
        return None
    else:
        return url_list[4]


def main():
    dictionary = {}
    script_directory = os.path.dirname(os.path.realpath(__file__))
    for i in tqdm(range(1, 623)):
        number = number_to_str(i, 5)
        url_prefix = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/mazowieckie/v1c9073l32'
        url_sufix = 'p1'
        url = ''.join([url_prefix, number, url_sufix])
        response = requests.get(url)
        region = extract_region(response.url)
        if region is not None:
            region = region.replace('+', '-')
            dictionary[region] = number
    print(dictionary)
    path = '/'.join([script_directory, 'gumtree_region_number_dict.json'])
    with open(file=path, mode='w') as fp:
        json.dump(dictionary, fp)


if __name__ == '__main__':
    main()
