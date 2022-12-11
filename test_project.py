import pytest
from project import get_output_directory_and_filename, should_add_zero_width_space, get_constant_type, Constants

def test_get_output_directory_and_filename():
    assert get_output_directory_and_filename("/workspaces/103347165/project/input/example.docx") == "/workspaces/103347165/project/output/example"
    assert get_output_directory_and_filename("/workspaces/103347165/project/input/တမန်တော်.docx") == "/workspaces/103347165/project/output/တမန်တော်"

def test_should_add_zero_width_space():
    assert should_add_zero_width_space('အ', 'က', 'ြ') == True
    assert should_add_zero_width_space('အ', 'မ', 'ျ') == True
    assert should_add_zero_width_space('း', 'မ', 'ျ') == True

    assert should_add_zero_width_space('က', 'ြ', 'ေ') == False
    assert should_add_zero_width_space('ာ', 'င', '်') == False
    assert should_add_zero_width_space('မ', 'ျ', 'ိ') == False

def test_get_constant_type():
    assert get_constant_type('က') == Constants.CONSONANTS_KEY
    assert get_constant_type('အ') == Constants.INDEPENDENT_VOWELS_KEY
    assert get_constant_type('ါ') == Constants.DEPENDENT_VOWEL_SIGNS_KEY
    assert get_constant_type('ံ') == Constants.VARIOUS_SIGNS_KEY
    assert get_constant_type('၎') == Constants.VARIOUS_SIGN_KEY
    assert get_constant_type('်') == Constants.VIRAMA_AND_KILLER_KEY
    assert get_constant_type('ျ') == Constants.DEPENDENT_CONSONANT_SIGNS_KEY
    assert get_constant_type('။') == Constants.PUNCTUATION_KEY
    assert get_constant_type('ဤ') == Constants.CUSTOM_STANDALONES_KEY