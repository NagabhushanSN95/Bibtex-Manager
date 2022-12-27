# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

import ast
import dataclasses
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from data_structures.entry_types.Generic import GenericEntry
from utils import MonthUtils, CommonUtils

JOURNAL_ABBREVIATION_PATTERN = r'(.+?) \((\w+)\)$'


@dataclass(eq=False)
class JournalEntry(GenericEntry):
    journal_full: str = None
    journal_short: str = None
    journal_abbreviation: str = None
    organization: str = None
    volume: str = None
    number: str = None
    pages: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = JournalEntry.extract_comment(raw_data)
        name = JournalEntry.extract_name(raw_data)
        fields_dict = JournalEntry.extract_fields(raw_data)
        journal_entry = JournalEntry(name=name)
        journal_entry.comment = comment
        journal_entry.title = fields_dict.get('title', None)
        journal_entry.author = fields_dict.get('author', None)
        journal_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        journal_entry.year = fields_dict.get('year', None)
        journal_entry.doi = fields_dict.get('doi', None)
        journal_entry.organization = fields_dict.get('organization', None)
        journal_entry.volume = fields_dict.get('volume', None)
        journal_entry.number = fields_dict.get('number', None)
        journal_entry.pages = fields_dict.get('pages', None)

        journal_data = JournalEntry.parse_journal(fields_dict.get('journal', None))
        journal_entry.journal_full = journal_data[0]
        journal_entry.journal_short = journal_data[1]
        journal_entry.journal_abbreviation = journal_data[2]
        return journal_entry

    @staticmethod
    def parse_journal(journal: str):
        if not journal:
            full_name = None
            short_name = None
            abbreviation = None
        else:
            matcher = re.match(JOURNAL_ABBREVIATION_PATTERN, journal)
            if matcher:
                journal = matcher.group(1)
                abbreviation = matcher.group(2)
            else:
                abbreviation = None

            short_forms = ['trans.']
            if any(short_form in journal.lower() for short_form in short_forms):
                short_name = journal
                full_name = None
            else:
                short_name = None
                full_name = journal
        return full_name, short_name, abbreviation

    def compose_journal(self, fields_names1: list):
        if 'journal_full' in fields_names1:
            if self.journal_full:
                journal = self.journal_full
            else:
                journal = self.journal_short
        elif 'journal_short' in fields_names1:
            if self.journal_short:
                journal = self.journal_short
            else:
                journal = self.journal_full
        elif 'journal_abbreviation' in fields_names1:
            if self.journal_abbreviation is None:
                journal = self.journal_full
            else:
                journal = self.journal_abbreviation
        else:
            return None
        if ('journal_abbreviation' in fields_names1) and self.journal_abbreviation:
            if ('journal_full' in fields_names1) or ('journal_short' in fields_names1):
                # This branch handles the case when short+abbr or full+abbr is used. Just abbr is handled in previous
                # branch
                journal += f' ({self.journal_abbreviation})'
        return journal

    def get_export_string(self, fields_names: list):
        lines = []
        if self.comment:
            lines.append(f'% {self.comment}')

        fields_dict = dataclasses.asdict(self)
        entry_name = fields_dict['name']
        lines.append(f'@article{{{entry_name},')

        if ('title' in fields_names) and self.title:
            lines.append(f'    title = {{{self.title}}},')
        if ('author' in fields_names) and self.author:
            lines.append(f'    author = {{{self.author}}},')
        journal_str = self.compose_journal(fields_names)
        if journal_str is not None:
            lines.append(f'    journal = {{{journal_str}}},')
        if ('volume' in fields_names) and self.volume:
            lines.append(f'    volume = {{{self.volume}}},')
        if ('number' in fields_names) and self.number:
            lines.append(f'    number = {{{self.number}}},')
        if ('pages' in fields_names) and self.pages:
            lines.append(f'    pages = {{{self.pages}}},')
        month_str = self.compose_month(fields_names)
        if month_str is not None:
            lines.append(f'    month = {{{month_str}}},')
        if ('year' in fields_names) and self.year:
            lines.append(f'    year = {{{self.year}}},')
        if ('doi' in fields_names) and self.doi:
            lines.append(f'    doi = {{{self.doi}}},')
        lines[-1] = lines[-1][:-1]  # Remove trailing comma
        lines.append('}')
        export_string = '\n'.join(lines)
        return export_string

    def fill_missing_data(self):
        self.fill_journal_names()

    def fill_journal_names(self):
        journals_data = self.get_journals_data()

        if not self.journal_full:
            if self.journal_short:
                journal_data = self.get_matching_journals_data(journals_data, self.journal_short, index=1)
                journal_data = CommonUtils.get_list_element(journal_data, 0)
            elif self.journal_abbreviation:
                journal_data = self.get_matching_journals_data(journals_data, self.journal_abbreviation, index=2)
                journal_data = CommonUtils.get_list_element(journal_data, 0)
            else:
                journal_data = None
            if journal_data and journal_data[0]:
                self.journal_full = journal_data[0]

        if not self.journal_short:
            if self.journal_full:
                journal_data = self.get_matching_journals_data(journals_data, self.journal_full, index=0)
                journal_data = CommonUtils.get_list_element(journal_data, 0)
            elif self.journal_abbreviation:
                journal_data = self.get_matching_journals_data(journals_data, self.journal_abbreviation, index=2)
                journal_data = CommonUtils.get_list_element(journal_data, 0)
            else:
                journal_data = None
            if journal_data and journal_data[1]:
                self.journal_short = journal_data[1]

        if not self.journal_abbreviation:
            if self.journal_full:
                journal_data = self.get_matching_journals_data(journals_data, self.journal_full, index=0)
                journal_data = CommonUtils.get_list_element(journal_data, 0)
            elif self.journal_short:
                journal_data = self.get_matching_journals_data(journals_data, self.journal_short, index=1)
                journal_data = CommonUtils.get_list_element(journal_data, 0)
            else:
                journal_data = None
            if journal_data and journal_data[2]:
                self.journal_abbreviation = journal_data[2]
    
    @staticmethod
    def get_journals_data():
        journal_data_path = Path('../res/short_forms/journals.txt')
        with open(journal_data_path.as_posix(), 'r') as journal_file:
            lines = journal_file.readlines()
        journals_data = [ast.literal_eval(line.strip()) for line in lines]
        return journals_data

    @staticmethod
    def get_matching_journals_data(journals_data: List[tuple], search_str: str, index: int):
        matching_journals_data = []
        for journal_data in journals_data:
            if journal_data[index] == search_str:
                matching_journals_data.append(journal_data)
        return matching_journals_data

    def check_inconsistencies(self):
        self.check_journal_inconsistencies()

    def check_journal_inconsistencies(self):
        def match_journal_(matching_journals_data_: List[tuple]):
            match_found = False
            if len(matching_journals_data_) == 0:
                match_found = True
            else:
                for matching_journal_data_ in matching_journals_data_:
                    if ((not matching_journal_data_[0]) or (self.journal_full == matching_journal_data_[0])) and \
                            ((not matching_journal_data_[1]) or (self.journal_short == matching_journal_data_[1])) and \
                            ((not matching_journal_data_[2]) or (self.journal_abbreviation == matching_journal_data_[2])):
                        match_found = True
            return match_found

        journals_data = self.get_journals_data()
        inconsistencies = False
        if self.journal_full:
            matching_journals_data = self.get_matching_journals_data(journals_data, self.journal_full, index=0)
            inconsistencies = inconsistencies or (not match_journal_(matching_journals_data))
        if self.journal_short:
            matching_journals_data = self.get_matching_journals_data(journals_data, self.journal_short, index=1)
            inconsistencies = inconsistencies or (not match_journal_(matching_journals_data))
        if self.journal_abbreviation:
            matching_journals_data = self.get_matching_journals_data(journals_data, self.journal_abbreviation, index=2)
            inconsistencies = inconsistencies or (not match_journal_(matching_journals_data))

        if inconsistencies:
            print(f'Inconsistencies found in journal for entry {self.name}.')
        return
