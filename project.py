import os
import sys
from docx import Document

def main():
    available_filenames = get_available_filenames()
    if len(available_filenames) == 0:
        print("There is no document in this directory.")
        return 

    selected_filename = select_filename(available_filenames)

    if selected_filename:
        process_docx(selected_filename)

    print("Have a nice day!")

def get_available_filenames():
    docxs = list()
    cur_dir_list = os.listdir()             # get all lists in current directory
    for docx in cur_dir_list:               # filter out docx files
        if docx.lower().endswith('.docx'):
            docxs.append(docx)

    return sorted(docxs);

def select_filename(docxs):
    print("\nHere are available documents in your current directory - ", end='\n\n')
    while True:
        for index, docx in enumerate(docxs):
            print(f"\t{index+1} - {docx}")
        print(f"\t{0} - Exit the program", end='\n\n')

        selected = int(input())
        if selected == 0:
            return None
        if len(docxs) >= selected: 
            return docxs[selected]

        print(f"Please enter a valid number (1 - {len(docxs)}) or exit code (0): ", end='')

def process_docx(filename):
    document = initialize_docx(filename)
    updatedDocument = add_zero_width_space(document)
    save_document(updatedDocument, filename)

def initialize_docx(filename):
    return Document(filename)

def add_zero_width_space(document):
    for p in document.paragraphs:
        for run in p.runs:
            para_list = list(map(str, run.text))               # Convert run.text to list
            for i in range(len(para_list)-2):
                if should_add_zero_width_space(para_list[i], para_list[i+1], para_list[i+2]):
                    para_list[i] = para_list[i]+u'\u200B'
            run.text = ''.join(map(str, para_list))

    return document

def save_document(document, filename):
    document.save(f"{get_only_filename(filename)}_ZWS.docx")

""" return selected document as a string """
def get_selection(docxs):
    for index, docx in enumerate(docxs):
        if docx == docxs[-1]:                     # if it's last element in the list
            print(f"\t{index+1} - {docx}")
            print(f"\t{0} - Exit the program", end='\n\n')
        else:
            print(f"\t{index+1} - {docx}")

    print(f"Enter a number (1 - {len(docxs)}) to select the document you want to modify: ", end='')

    while True:
        try:
            select = int(input())
            if select == 0:
                return None
            elif select in range(1, len(docxs)+1):
                return docxs[select-1]
            else:
                raise ValueError
        except ValueError:
            print(f"Please enter a valid number (1 - {len(docxs)}) or exit code (0): ", end='')

def get_only_filename(docx):
    return docx.replace(".docx", "")

def should_add_zero_width_space(first, second, third):
    first = get_constant_type(first)
    second = get_constant_type(second)
    third = get_constant_type(third)
    
    if ((first == Constants.CUSTOM_STANDALONES_KEY) 
        or (second == Constants.CUSTOM_STANDALONES_KEY 
        and (not third == "Punctuation"))):
                return True
    elif ((first == "Consonants" or first == "Independent_vowels")
        and (second == "Consonants")
        and (not third == "Virama_and_killer")):
        return True
    elif ((first == "Consonants")
        and (second == "Independent_vowels")
        and (not third == "Consonants")):
        return True
    elif ((first == "Various_signs")
        and (second == "Consonants")
        and (third == "Dependent_vowel_signs")):
        return True
    elif ((first == "Dependent_vowel_signs")
        and (second == "Consonants")
        and (third == "Dependent_vowel_signs" or third == "Consonants" or third == "Various_signs")):
        return True
    elif ((first == "Virama_and_killer")
        and (second == "Consonants")
        and (third == "Dependent_vowel_signs" or third == "Dependent_consonant_signs")):
        return True
    elif ((first == "Virama_and_killer")
        and (second == "Consonants")
        and (third == "Various_signs")):
        return True
    elif ((first == "Various_signs")
        and (second == "Consonants")
        and (third == "Dependent_consonant_signs")):
        return True
    elif ((first == "Virama_and_killer")
        and (second == "Consonants" or second == "Independent_vowels")
        and (third == "Consonants")):
        return True
    elif ((first == "Dependent_vowel_signs")
        and (second == "Consonants")
        and (third == "Dependent_consonant_signs")):
        return True
    elif ((first == "Dependent_vowel_signs")
        and (second == "Independent_vowels")
        and (third == "Consonants")):
        return True
    elif ((first == "Various_signs" or first == "Dependent_consonant_signs")
        and (second == "Consonants")
        and (third == "Consonants")):
        return True
    elif ((first == "Dependent_vowel_signs")
        and (second == "Consonants")
        and (third == "Consonants" or third == "Independent_vowels")):
        return True
    elif ((first == "Dependent_consonant_signs")
        and (second == "Consonants")
        and (third == "Dependent_vowel_signs")):
        return True
    elif ((first == "Various_signs")
        and (second == "Independent_vowels")
        and (third == "Consonants" or third == "Dependent_vowel_signs")):
        return True
    elif ((first == "Various_SIGNS")
        and (not second == "Consonants")):
        return True

    return False

def get_constant_type(char):
    constant_type = None
    if char in Constants.Consonants:
        constant_type = "Consonants"
    elif char in Constants.Independent_vowels:
        return "Independent_vowels"
    elif char in Constants.Dependent_vowel_signs:
        return "Dependent_vowel_signs"
    elif char in Constants.Various_signs:
        return "Various_signs"
    elif char in Constants.Various_SIGNS:
        return "Various_SIGNS"
    elif char == Constants.Virama_and_killer[1]:  # Virama_and_killer[0] is exception character
        return "Virama_and_killer"
    elif char in Constants.Dependent_consonant_signs:
        return "Dependent_consonant_signs"
    elif char in Constants.Punctuation:
        return "Punctuation"
    elif char in Constants.CUSTOM_STANDALONES_VALUES:
        return Constants.CUSTOM_STANDALONES_KEY

    return constant_type

class Constants:
    # https://unicode-table.com/en/blocks/myanmar/

    Consonants =   ['က','ခ','ဂ','ဃ','င','စ','ဆ','ဇ','ဈ','ဉ','ည',
                    'ဋ','ဌ','ဍ','ဎ','ဏ','တ','ထ','ဒ','ဓ','န','ပ',
                    'ဖ','ဗ','ဘ','မ','ယ','ရ','လ','ဝ','သ','ဟ','ဠ']

    Independent_vowels = ['အ','ဢ','ဥ','ဦ','ဧ','ဨ','ဩ']

    Dependent_vowel_signs = ['ါ','ာ','ိ','ီ','ု','ူ','ေ','ဲ','ဳ','ဴ','ဵ']

    Various_signs = ['ံ','့','း']

    Virama_and_killer = ['္','်']

    Dependent_consonant_signs = ['ျ','ြ','ွ','ှ']

    # Consonant = ['ဿ']

    Digits = ['၀','၁','၂','၃','၄','၅','၆','၇','၈','၉']

    Punctuation = ['၊','။']

    Various_SIGNS = ['၎']

    CUSTOM_STANDALONES_KEY = 'custom_standalones'
    CUSTOM_STANDALONES_VALUES = ['ဤ','ဪ','၌','၍','၏','ဣ','ဿ']

if __name__ == "__main__":
    main()
