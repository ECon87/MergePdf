#! /user/bin/env /home/econ87/venvs/GenPurpose/bin/python3

import PyPDF2
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyWordCompleter
from os import listdir
from pathlib import Path
import re

# Get recursive directory contents based on current directory
path = '.'

# contents = []


def get_all_pdfs(path:str, contents:list)->list:
    """
    Gets a list of all pdsf in the path.
    """
    for subpath in Path(path).iterdir():
        contents.append(subpath)
        if subpath.is_dir():
            get_all_pdfs(subpath, contents)
    contents = sorted([str(f) for f in contents])
    contents = sorted([f for f in contents if re.search('\.pdf$', f)])
    return contents


def fuzzy_selection(contents:list)->str:
    """
    Fuzzy prompt to select among the available pdfs.
    Called in select_pdf function and returns a single choice.
    """
    contents = sorted(list(set(contents)))
    # values_completer = WordCompleter(contents)
    values_completer = FuzzyWordCompleter(contents)
    # prompt('> ', completer=values_completer)
    choice = prompt('> ', completer=values_completer)
    return choice



def select_pdf(path:str, chosenpdf:list):
    contents = []
    all_files = get_all_pdfs(path, contents)
    choice = fuzzy_selection(contents=all_files)
    if choice == 'end':
        return chosenpdf
    else:
        chosenpdf.append(choice)
        print(f"Added {choice}\n")
        select_pdf(path, chosenpdf)


def merge_files(path):
    choices = []
    print("Select files to merge. Enter 'end' to exit!\n")
    select_pdf(path, chosenpdf=choices)
    print("\nYou have selected:")
    for j, c in enumerate(choices):
        print(j, c)
    verify = input("\nAre you ok with this order? (y/n) ")
    if verify == "y":
        pass
    else:
        new_order = input("\nRe-order without spaces (eg. 1,2,3..)")
        new_order = new_order.split(",")
        new_order = [int(j)-1 for j in new_order]
        choices2 = [choices[j] for j in new_order]
        choices = choices2
    merger = PyPDF2.PdfFileMerger()
    for f in choices:
        merger.append(PyPDF2.PdfFileReader(f'{f}', 'rb'))
    name_to_save = input("\nEnter path and filename (ignore file extension): ")
    merger.write(f"{name_to_save}.pdf")


if __name__ == "__main__":
    merge_files(path)
