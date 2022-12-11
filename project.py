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
        process_docx(f'{os.getcwd()}/input/{selected_filename}')
        print("Your modified document has been generated in output folder of current directory.")

    print("Have a nice day!")

""" ******* MAIN ENDS HERE ******* """

def get_available_filenames():
    docxs = list()
    cur_dir_list = os.listdir(f'{os.getcwd()}/input')       # get all lists in input folder of current directory
    for docx in cur_dir_list:               # filter out docx files
        if docx.lower().endswith('.docx'):
            docxs.append(docx)

    return sorted(docxs)

def select_filename(docxs):
    print("Here are available documents in your current directory - ", end='\n\n')
    for index, docx in enumerate(docxs):
        print(f"\t{index+1} - {docx}")
    print(f"\t{0} - Exit the program", end='\n\n')
    print(f"Enter a number (1 - {len(docxs)}) to select the document you want to modify: ", end='')
    while True:
        try:
            selected = int(input().strip())
            if selected == 0:
                return None
            if len(docxs) >= selected:
                return docxs[selected-1]        # return selected filename as a string
            else:
                raise ValueError

        except ValueError:
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
    filename = f"{get_output_directory_and_filename(filename)}_ZWS.docx"
    document.save(filename)

def get_output_directory_and_filename(docx):
    return docx.replace("input", 'output').replace(".docx", "")

def should_add_zero_width_space(first, second, third):
    first = get_constant_type(first)
    second = get_constant_type(second)
    third = get_constant_type(third)

    should_add = False

    if ((first == Constants.CUSTOM_STANDALONES_KEY) or
        (second == Constants.CUSTOM_STANDALONES_KEY
        and (not third == Constants.PUNCTUATION_KEY))):
        should_add = True
    elif ((first == Constants.CONSONANTS_KEY or
        first == Constants.INDEPENDENT_VOWELS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (not third == Constants.VIRAMA_AND_KILLER_KEY)):
        should_add = True
    elif ((first == Constants.CONSONANTS_KEY)
        and (second == Constants.INDEPENDENT_VOWELS_KEY)
        and (not third == Constants.CONSONANTS_KEY)):
        should_add = True
    elif ((first == Constants.VARIOUS_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.DEPENDENT_VOWEL_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.DEPENDENT_VOWEL_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.DEPENDENT_VOWEL_SIGNS_KEY or
        third == Constants.CONSONANTS_KEY or
        third == Constants.VARIOUS_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.VIRAMA_AND_KILLER_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.DEPENDENT_VOWEL_SIGNS_KEY or
        third == Constants.DEPENDENT_CONSONANT_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.VIRAMA_AND_KILLER_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.VARIOUS_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.VARIOUS_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.DEPENDENT_CONSONANT_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.VIRAMA_AND_KILLER_KEY)
        and (second == Constants.CONSONANTS_KEY or
        second == Constants.INDEPENDENT_VOWELS_KEY)
        and (third == Constants.CONSONANTS_KEY)):
        should_add = True
    elif ((first == Constants.DEPENDENT_VOWEL_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.DEPENDENT_CONSONANT_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.DEPENDENT_VOWEL_SIGNS_KEY)
        and (second == Constants.INDEPENDENT_VOWELS_KEY)
        and (third == Constants.CONSONANTS_KEY)):
        should_add = True
    elif ((first == Constants.VARIOUS_SIGNS_KEY or
        first == Constants.DEPENDENT_CONSONANT_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.CONSONANTS_KEY)):
        should_add = True
    elif ((first == Constants.DEPENDENT_VOWEL_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.CONSONANTS_KEY or
        third == Constants.INDEPENDENT_VOWELS_KEY)):
        should_add = True
    elif ((first == Constants.DEPENDENT_CONSONANT_SIGNS_KEY)
        and (second == Constants.CONSONANTS_KEY)
        and (third == Constants.DEPENDENT_VOWEL_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.VARIOUS_SIGNS_KEY)
        and (second == Constants.INDEPENDENT_VOWELS_KEY)
        and (third == Constants.CONSONANTS_KEY or
        third == Constants.DEPENDENT_VOWEL_SIGNS_KEY)):
        should_add = True
    elif ((first == Constants.VARIOUS_SIGN_KEY)
        and (not second == Constants.CONSONANTS_KEY)):
        should_add = True

    return should_add

def get_constant_type(char):
    constant_type = None
    if char in Constants.CONSONANTS_VALUES:
        constant_type = Constants.CONSONANTS_KEY
    elif char in Constants.INDEPENDENT_VOWELS_VALUES:
        constant_type = Constants.INDEPENDENT_VOWELS_KEY
    elif char in Constants.DEPENDENT_VOWEL_SIGNS_VALUES:
        constant_type = Constants.DEPENDENT_VOWEL_SIGNS_KEY
    elif char in Constants.VARIOUS_SIGNS_VALUES:
        constant_type = Constants.VARIOUS_SIGNS_KEY
    elif char in Constants.VARIOUS_SIGN_VALUES:
        constant_type = Constants.VARIOUS_SIGN_KEY
    elif char in Constants.VIRAMA_AND_KILLER_VALUES:
        constant_type = Constants.VIRAMA_AND_KILLER_KEY
    elif char in Constants.DEPENDENT_CONSONANT_SIGNS_VALUES:
        constant_type = Constants.DEPENDENT_CONSONANT_SIGNS_KEY
    elif char in Constants.PUNCTUATION_VALUES:
        constant_type = Constants.PUNCTUATION_KEY
    elif char in Constants.CUSTOM_STANDALONES_VALUES:
        constant_type = Constants.CUSTOM_STANDALONES_KEY

    return constant_type

class Constants:
    # https://unicode-table.com/en/blocks/myanmar/

    CONSONANTS_KEY = 'Consonants'
    CONSONANTS_VALUES = ['က','ခ','ဂ','ဃ','င','စ','ဆ','ဇ','ဈ','ဉ','ည',
                        'ဋ','ဌ','ဍ','ဎ','ဏ','တ','ထ','ဒ','ဓ','န','ပ',
                        'ဖ','ဗ','ဘ','မ','ယ','ရ','လ','ဝ','သ','ဟ','ဠ']

    INDEPENDENT_VOWELS_KEY = 'Independent_vowels'
    INDEPENDENT_VOWELS_VALUES = ['အ','ဢ','ဥ','ဦ','ဧ','ဨ','ဩ']

    DEPENDENT_VOWEL_SIGNS_KEY = 'Dependent_vowel_signs'
    DEPENDENT_VOWEL_SIGNS_VALUES = ['ါ','ာ','ိ','ီ','ု','ူ','ေ','ဲ','ဳ','ဴ','ဵ']

    VARIOUS_SIGNS_KEY = 'Various_signs'
    VARIOUS_SIGNS_VALUES = ['ံ','့','း']

    VIRAMA_AND_KILLER_KEY = 'Virama_and_killer'
    VIRAMA_AND_KILLER_VALUES = ['်'] # ['္', '်'] # Virama_and_killer[0] is exception character

    DEPENDENT_CONSONANT_SIGNS_KEY = 'Dependent_consonant_signs'
    DEPENDENT_CONSONANT_SIGNS_VALUES = ['ျ','ြ','ွ','ှ']

    DIGITS_KEY = 'Digits'
    DIGITS_VALUES = ['၀','၁','၂','၃','၄','၅','၆','၇','၈','၉']

    PUNCTUATION_KEY = 'Punctuation'
    PUNCTUATION_VALUES = ['၊','။']

    VARIOUS_SIGN_KEY = 'Various_SIGN'
    VARIOUS_SIGN_VALUES = ['၎']

    CUSTOM_STANDALONES_KEY = 'custom_standalones'
    CUSTOM_STANDALONES_VALUES = ['ဤ','ဪ','၌','၍','၏','ဣ','ဿ']

if __name__ == "__main__":
    main()
