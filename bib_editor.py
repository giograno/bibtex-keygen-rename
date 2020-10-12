import sys
import subprocess
import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
from collections import defaultdict
import fileinput
import glob


def main(original_bibtex_path: str):
    new_bibtex_path: str = os.path.join(os.path.dirname(original_bibtex_path), 'new_bib.bib')
    print(new_bibtex_path)
    command: str = 'bibtool -k {} -o {}'.format(original_bibtex_path, new_bibtex_path)
    process = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, stderr = process.communicate()
    print("Warnings or errors: \n{}".format(stderr))

    with open(original_bibtex_path, encoding='latin-1') as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = homogenize_latex_encoding
        original_db = bibtexparser.load(bibtex_file, parser=parser)

    with open(new_bibtex_path, encoding='latin-1') as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = homogenize_latex_encoding
        new_db = bibtexparser.load(bibtex_file, parser=parser)

    keys_match = defaultdict()
    for key, val in original_db.entries_dict.items():
        original_title = val['title']
        for new_key, new_val in new_db.entries_dict.items():
            new_title = new_val['title']
            if original_title == new_title:
                keys_match[key] = new_key

    tex_files = glob.glob('{}/**/*.tex'.format(os.path.dirname(original_bibtex_path)), recursive=True)
    for original_key, new_key in keys_match.items():
        print('{} -> {}'.format(original_key, new_key))
        for line in fileinput.input(tex_files, inplace=True):
            print(line.replace(original_key, new_key), end="")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        bib_path = sys.argv[1]
    else:
        bib_path = '/Users/giograno/Desktop/developer-based-unit-test-quality/biblio.bib'
    main(bib_path)
