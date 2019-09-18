from housy.processing.text_processing import calculate_intersection, get_processed_text, extract_date


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
