from housy.processing.text_processing import calculate_intersection, get_processed_text, extract_date, extract_from_tag, \
    olx_convert_to_time_struct
from parsedatetime import Calendar


def test_processed_text_handles_empty_list():
    test_list = []
    assert get_processed_text(test_list) == ''


def test_processed_text_handles_none():
    test_list = None
    assert get_processed_text(test_list) == ''


def test_processed_text_handles_normal_case():
    test_list = ['  Lalunia', 'Łabędź   ', 'xD']
    assert get_processed_text(test_list) == 'lalunia labedz xd'


def test_intersection_of_empty_list():
    words_to_search = []
    text_to_search_in = 'that\'s a whole bunch of text'
    assert calculate_intersection(text_to_search_in, words_to_search) == 1.0


def test_intersection_of_normal_use_case():
    words_to_search = ['one']
    text_to_search_in = 'that\'s a whole bunch of text'
    assert calculate_intersection(text_to_search_in, words_to_search) == 0.0


def test_extract_date_from_polish_from_7_minutes_ago():
    test_input = '<div class="creation-date"><span>7 minut temu</span></div>'
    assert extract_date(test_input) == '7 minutes ago'


def test_extract_date_from_polish_from_1_minutes_ago():
    test_input = '<div class="creation-date"><span>minutę temu</span></div>'
    assert extract_date(test_input) == '1 minutes ago'


def test_extract_date_from_polish_from_3_minutes_ago():
    test_input = '<div class="creation-date"><span>3 minuty temu</span></div>'
    assert extract_date(test_input) == '3 minutes ago'


def test_extract_date_from_polish_since_one_hour():
    test_input = '<div class="creation-date"><span>godzinę temu</span></div>'
    assert extract_date(test_input) == '1 hours ago'


def test_extract_date_from_polish_since_5_hours():
    test_input = '<div class="creation-date"><span>5 godzin temu</span></div>'
    assert extract_date(test_input) == '5 hours ago'


def test_extract_date_from_polish_since_3_hours():
    test_input = '<div class="creation-date"><span>3 godziny temu</span></div>'
    assert extract_date(test_input) == '3 hours ago'


def test_extract_date_from_polish_since_12_hours():
    test_input = '<div class="creation-date"><span>12 godziny temu</span></div>'
    assert extract_date(test_input) == '12 hours ago'


def test_extract_date_from_polish_from_1_day_ago():
    test_input = '<div class="creation-date"><span>1 dzień temu</span></div>'
    assert extract_date(test_input) == '1 days ago'


def test_extract_date_from_polish_from_2_days_ago():
    test_input = '<div class="creation-date"><span>2 dni temu</span></div>'
    assert extract_date(test_input) == '2 days ago'


def test_extracts_from_tag_properly_valid_case():
    test_input = '<div class="some boring class md col whatever">this is an important message</div>'
    assert extract_from_tag(test_input) == 'this is an important message'


def test_olx_convert_to_time_struct_valid_case():
    test_input = {
        'dzisiaj 13:48': 'today 13:48',
        'wczoraj 13:48': 'yesterday 13:48',
        '16 sty': '16 january',
        '16 wrz': '16 september',
        '16 lut': '16 february',
        '16 mar': '16 march',
        '16 kwi': '16 april',
        '16 maj': '16 may',
        '16 cze': '16 june',
        '16 lip': '16 july',
        '16 sie': '16 august',
        '16 paź': '16 october',
        '16 lis': '16 november',
        '16 gru': '16 december',
    }
    cal = Calendar()
    for k, v in test_input.items():
        assert olx_convert_to_time_struct(k) == cal.parse(v)[0]
