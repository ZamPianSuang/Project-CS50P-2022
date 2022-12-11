import pytest
from project import get_only_filename, get_type, manager, get_selection

def test_get_only_filename():
    assert get_only_filename("example1.docx") == "example1"
    assert get_only_filename("တမန်တော်.docx") == "တမန်တော်"

def test_manager():
    assert manager('အ', 'က', 'ြ') == True
    assert manager('အ', 'မ', 'ျ') == True
    assert manager('း', 'မ', 'ျ') == True

    assert manager('က', 'ြ', 'ေ') == None
    assert manager('ာ', 'င', '်') == None
    assert manager('မ', 'ျ', 'ိ') == None

def test_get_type():
    assert get_type('က') == "Consonants"
    assert get_type('အ') == "Independent_vowels"
    assert get_type('ါ') == "Dependent_vowel_signs"
    assert get_type('ံ') == "Various_signs"
    assert get_type('၎') == "Various_SIGNS"
    assert get_type('်') == "Virama_and_killer"
    assert get_type('ျ') == "Dependent_consonant_signs"
    assert get_type('။') == "Punctuation"
    assert get_type('ဤ') == "custom_standalones"