from housy.processing.text_processing import calculate_intersection, get_processed_text


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
