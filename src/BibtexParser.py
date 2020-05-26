# Shree KRISHNAya Namaha
# Parses an existing bibtex file and adds to the data
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

from pathlib import Path
from typing import List

from data_structures.EntryCollection import EntryCollection
from data_structures.entry_types.EntryFactory import EntryFactory


class BibtexIterator:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.remove_doc_comments()
        return

    def __iter__(self):
        return self

    def __next__(self):
        if not self.lines:
            raise StopIteration
        line = self.lines.pop(0)
        entry_lines = []
        while line != '}':
            if line:
                entry_lines.append(line)
            line = self.lines.pop(0)
        entry_lines.append(line)
        return entry_lines

    def remove_doc_comments(self):
        num_comment_lines = 0
        for line in self.lines:
            if not line or line.lstrip().startswith('%'):
                num_comment_lines += 1
            else:
                break
        self.lines = self.lines[num_comment_lines:]
        return


def main():
    bibtex_filepath = Path('C:/Users/nagab/Desktop/bibtex.bib')
    with open(bibtex_filepath.as_posix(), 'r') as bibtex_file:
        lines = bibtex_file.readlines()
        lines = [line.rstrip() for line in lines]
    bibtex_iterator = BibtexIterator(lines)

    entries = EntryCollection()
    for raw_entry in bibtex_iterator:
        parsed_entry = EntryFactory.raw2entry(raw_entry)
        if parsed_entry:
            entries.add_entry(parsed_entry)
        else:
            print('Warning! Found None while parsing bib file')
    entries.refresh()
    entries.save_to_disk()
    return


if __name__ == '__main__':
    main()
