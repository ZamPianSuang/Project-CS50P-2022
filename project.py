import os
import sys
from docx import Document

def main():
    """ Get available documents from current directory """
    available_docxs = get_docx()

    print("\nHere are available documents in your current directory - ", end='\n\n')

    for index, docx in enumerate(available_docxs):
        if docx == available_docxs[-1]:                     # if it's last element in the list
            print(f"\t{index+1} - {docx}")
            print(f"\t{0} - Exit the program", end='\n\n')
        else:
            print(f"\t{index+1} - {docx}")

    print(f"Enter a number (1 - {len(available_docxs)}) to select the document you want to modify: ", end='')

    """ Get user selection of document """
    selected_doc = get_selection(available_docxs)

    document = Document(selected_doc)

    for p in document.paragraphs:
        for run in p.runs:
            para_list = list(map(str, run.text))               # Convert run.text to list
            for i in range(len(para_list)-2):
                if manager(para_list[i], para_list[i+1], para_list[i+2]):
                    para_list[i] = para_list[i]+u'\u200B'
            run.text = ''.join(map(str, para_list))

    document.save(f"{get_only_filename(selected_doc)}_ZWS.docx")


""" ******* MAIN ENDS HERE ******* """

def get_docx():
    docxs = list()
    cur_dir_list = os.listdir()             # get all lists in current directory
    for docx in cur_dir_list:               # filter out docx files
        if docx.lower().endswith('.docx'):
            docxs.append(docx)

    if not docxs:
        sys.exit("There is no document in this directory.")
    else:
        docxs = sorted(docxs)
        return docxs

""" return selected document as a string """
def get_selection(docxs):
    while True:
        try:
            select = int(input())
            if select == 0:
                sys.exit("Have a nice day!")
            elif select in range(1, len(docxs)+1):
                return docxs[select-1]
            else:
                raise ValueError
        except ValueError:
            print(f"Please enter a valid number (1 - {len(docxs)}) or exit code (0): ", end='')

def get_only_filename(docx):
    return docx.replace(".docx", "")

def manager(first, second, third):
    first = get_type(first)
    second = get_type(second)
    third = get_type(third)
    if ((first == "custom_standalones")
        or (second == "custom_standalones" and (not third == "Punctuation"))):
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

def get_type(char):
    if char in constants.Consonants:
        return "Consonants"
    elif char in constants.Independent_vowels:
        return "Independent_vowels"
    elif char in constants.Dependent_vowel_signs:
        return "Dependent_vowel_signs"
    elif char in constants.Various_signs:
        return "Various_signs"
    elif char in constants.Various_SIGNS:
        return "Various_SIGNS"
    elif char == constants.Virama_and_killer[1]:  # Virama_and_killer[0] is exception character
        return "Virama_and_killer"
    elif char in constants.Dependent_consonant_signs:
        return "Dependent_consonant_signs"
    elif char in constants.Punctuation:
        return "Punctuation"
    elif char in constants.custom_standalones:
        return "custom_standalones"

class constants:
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

    custom_standalones = ['ဤ','ဪ','၌','၍','၏','ဣ','ဿ']

if __name__ == "__main__":
    main()
