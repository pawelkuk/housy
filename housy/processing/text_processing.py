from unidecode import unidecode
from parsedatetime import Calendar
import re


def get_processed_text(list_of_str):
    """Storing str in list to avoid memory coping."""
    tmp_list = []
    if list_of_str is not None:
        for raw_str_bit in list_of_str:
            accented_str_bit = raw_str_bit.strip().lower()
            str_bit = unidecode(accented_str_bit)
            tmp_list.append(str_bit)
        return ' '.join(tmp_list)
    else:
        return ''


def calculate_intersection(text_to_look_through, words_to_search):
    number_of_words_to_search = len(words_to_search)
    number_of_words_present = sum([1 for word in words_to_search if word in text_to_look_through])
    return number_of_words_present / number_of_words_to_search if number_of_words_to_search > 0 else 1.0


def extract_date(gumtree_unprocessed_date):
    translation = {
        'minutę': 'minutes',
        'minuty': 'minutes',
        'minut': 'minutes',
        'godzinę': 'hours',
        'godziny': 'hours',
        'godzin': 'hours',
        'dzień': 'days',
        'dni': 'days',
    }
    time_in_polish = gumtree_unprocessed_date.split('span>')[1]
    time_list = time_in_polish.split(' ')
    if len(time_list) == 2:
        return ' '.join(['1', translation[time_list[0]], 'ago'])
    else:
        return ' '.join([time_list[0], translation[time_list[1]], 'ago'])


def extract_from_tag(text_in_tag):
    return re.sub(r'<(div|/div|br|p|/p|span|/span)[^>]*>', '', text_in_tag)


def morizon_convert_to_time_struct(date_str):
    morizon_date_mapper = {
        'dzisiaj': 'today',
        'wczoraj': 'yesterday'
    }
    cal = Calendar()
    date_str = morizon_date_mapper[date_str] if date_str in morizon_date_mapper else date_str
    return cal.parse(date_str)[0]
