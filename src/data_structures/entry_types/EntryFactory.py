# Shree KRISHNAya Namaha
# A Factory class to create entries from json
# Author: Nagabhushan S N
# Last Modified: 26-04-2020

from typing import List

from src.data_structures.entry_types.Book import BookEntry
from src.data_structures.entry_types.Conference import ConferenceEntry
from src.data_structures.entry_types.Journal import JournalEntry
from src.data_structures.entry_types.Misc import MiscEntry
from src.data_structures.entry_types.TechReport import TechReportEntry
from src.data_structures.entry_types.arXiv import arXivEntry
from src.data_structures.entry_types.bioRxiv import bioRxivEntry


class EntryFactory:
    @staticmethod
    def dict2entry(entry_dict: dict):
        """
        This is used for loading the data from disk
        """
        class_name = entry_dict['class_name']
        classes = [ConferenceEntry, JournalEntry, arXivEntry, bioRxivEntry, TechReportEntry, BookEntry, MiscEntry]
        for klass in classes:
            if class_name == klass.__name__:
                return klass.from_dict(entry_dict)

    @staticmethod
    def raw2entry(raw_entry: List[str]):
        """
        This is used when parsing a bibtex file
        """
        first_line = None
        for line in raw_entry:
            if line.startswith('%'):
                continue
            else:
                first_line = line.lstrip().lower()
                break
        if first_line.startswith('@inproceedings'):
            return ConferenceEntry.parse_raw_data(raw_entry)
        elif first_line.startswith('@article'):
            # Check journal field to differentiate between arXiv, bioRxiv and journals
            journal_line = ''
            for line in raw_entry:
                if 'journal' in line:
                    journal_line = line.strip().lower()
                    break
            if 'arxiv' in journal_line:
                return arXivEntry.parse_raw_data(raw_entry)
            elif 'biorxiv' in journal_line:
                return bioRxivEntry.parse_raw_data(raw_entry)
            else:
                return JournalEntry.parse_raw_data(raw_entry)
        elif first_line.startswith('@techreport'):
            return TechReportEntry.parse_raw_data(raw_entry)
        elif first_line.startswith('@book'):
            return BookEntry.parse_raw_data(raw_entry)
        elif first_line.startswith('@misc'):
            return MiscEntry.parse_raw_data(raw_entry)
        else:
            # TODO: Uncomment this
            # raise RuntimeError(f'Unable to parse entry of type "{first_line}"')
            return None
