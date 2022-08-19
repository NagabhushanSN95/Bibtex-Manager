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
from utils import MonthUtils

BOOKTITLE_ABBREVIATION_PATTERN = r'(.+?) \(([\w-]+)\)$'


@dataclass(eq=False)
class ConferenceEntry(GenericEntry):
    booktitle_full: str = None
    booktitle_short: str = None
    booktitle_abbreviation: str = None
    organization: str = None
    pages: str = None
    volume: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = ConferenceEntry.extract_comment(raw_data)
        name = ConferenceEntry.extract_name(raw_data)
        fields_dict = ConferenceEntry.extract_fields(raw_data)
        conf_entry = ConferenceEntry(name=name)
        conf_entry.comment = comment
        conf_entry.title = fields_dict.get('title', None)
        conf_entry.author = fields_dict.get('author', None)
        conf_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        conf_entry.year = fields_dict.get('year', None)
        conf_entry.doi = fields_dict.get('doi', None)
        conf_entry.organization = fields_dict.get('organization', None)
        conf_entry.pages = fields_dict.get('pages', None)
        conf_entry.volume = fields_dict.get('volume', None)

        booktitle_data = ConferenceEntry.parse_booktitle(fields_dict.get('booktitle', None))
        conf_entry.booktitle_full = booktitle_data[0]
        conf_entry.booktitle_short = booktitle_data[1]
        conf_entry.booktitle_abbreviation = booktitle_data[2]
        return conf_entry

    @staticmethod
    def parse_booktitle(booktitle: str):
        if not booktitle:
            full_name = None
            short_name = None
            abbreviation = None
        else:
            matcher = re.match(BOOKTITLE_ABBREVIATION_PATTERN, booktitle)
            if matcher:
                booktitle = matcher.group(1)
                abbreviation = matcher.group(2)
            else:
                abbreviation = None

            short_forms = ['conf.']
            if any(short_form in booktitle.lower() for short_form in short_forms):
                short_name = booktitle
                full_name = None
            else:
                short_name = None
                full_name = booktitle
        return full_name, short_name, abbreviation

    def compose_booktitle(self, fields_names1: list):
        if 'booktitle_full' in fields_names1:
            if self.booktitle_full:
                booktitle = self.booktitle_full
            else:
                booktitle = self.booktitle_short
            if (booktitle is not None) and ('proceedings' in fields_names1):
                booktitle = 'Proceedings of the ' + booktitle
        elif 'booktitle_short' in fields_names1:
            if self.booktitle_short:
                booktitle = self.booktitle_short
            else:
                booktitle = self.booktitle_full
            if (booktitle is not None) and ('proceedings' in fields_names1):
                booktitle = 'Proc. ' + booktitle
        elif 'booktitle_abbreviation' in fields_names1:
            if self.booktitle_abbreviation is None:
                booktitle = self.booktitle_full
            else:
                booktitle = self.booktitle_abbreviation
            if (booktitle is not None) and ('proceedings' in fields_names1):
                booktitle = 'Proc. ' + booktitle
        else:
            return None
        if 'booktitle_abbreviation' in fields_names1 and self.booktitle_abbreviation:
            if ('booktitle_full' in fields_names1) or ('booktitle_short' in fields_names1):
                # This branch handles the case when short+abbr or full+abbr is used. Just abbr is handled in previous
                # branch
                booktitle += f' ({self.booktitle_abbreviation})'
        return booktitle

    def get_export_string(self, fields_names: list):
        lines = []
        if self.comment:
            lines.append(f'% {self.comment}')

        fields_dict = dataclasses.asdict(self)
        entry_name = fields_dict['name']
        lines.append(f'@inproceedings{{{entry_name},')

        if ('title' in fields_names) and self.title:
            lines.append(f'    title = {{{self.title}}},')
        if ('author' in fields_names) and self.author:
            lines.append(f'    author = {{{self.author}}},')
        if self.compose_booktitle(fields_names):
            lines.append(f'    booktitle = {{{self.compose_booktitle(fields_names)}}},')
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
        self.fill_booktitle_names()

    def fill_booktitle_names(self):
        booktitles_data = self.get_booktitles_data()

        if not self.booktitle_full:
            if self.booktitle_short:
                booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_short, index=1)
            elif self.booktitle_abbreviation:
                booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_abbreviation, index=2)
            else:
                booktitle_data = None
            if booktitle_data and booktitle_data[0]:
                self.booktitle_full = booktitle_data[0]

        if not self.booktitle_short:
            if self.booktitle_full:
                booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_full, index=0)
            elif self.booktitle_abbreviation:
                booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_abbreviation, index=2)
            else:
                booktitle_data = None
            if booktitle_data and booktitle_data[1]:
                self.booktitle_short = booktitle_data[1]

        if not self.booktitle_abbreviation:
            if self.booktitle_full:
                booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_full, index=0)
            elif self.booktitle_short:
                booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_short, index=1)
            else:
                booktitle_data = None
            if booktitle_data and booktitle_data[2]:
                self.booktitle_abbreviation = booktitle_data[2]

    @staticmethod
    def get_booktitles_data():
        booktitle_data_path = Path('../res/short_forms/conferences.txt')
        with open(booktitle_data_path.as_posix(), 'r') as booktitle_file:
            lines = booktitle_file.readlines()
        booktitles_data = [ast.literal_eval(line.strip()) for line in lines]
        return booktitles_data

    @staticmethod
    def get_matching_booktitle_data(booktitles_data: List[tuple], search_str: str, index: int):
        for booktitle_data in booktitles_data:
            if booktitle_data[index] == search_str:
                return booktitle_data
        return None

    def check_inconsistencies(self):
        self.check_booktitle_inconsistencies()

    def check_booktitle_inconsistencies(self):
        def match_booktitle(booktitle_data1: tuple):
            if booktitle_data1:
                if (booktitle_data1[0] and (self.booktitle_full != booktitle_data1[0])) or \
                        (booktitle_data1[1] and (self.booktitle_short != booktitle_data1[1])) or \
                        (booktitle_data1[2] and (self.booktitle_abbreviation != booktitle_data1[2])):
                    return True
            return False

        booktitles_data = self.get_booktitles_data()
        inconsistencies = False
        if self.booktitle_full:
            booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_full, index=0)
            inconsistencies = inconsistencies or match_booktitle(booktitle_data)
        if self.booktitle_short:
            booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_short, index=1)
            inconsistencies = inconsistencies or match_booktitle(booktitle_data)
        if self.booktitle_abbreviation:
            booktitle_data = self.get_matching_booktitle_data(booktitles_data, self.booktitle_abbreviation, index=2)
            inconsistencies = inconsistencies or match_booktitle(booktitle_data)

        if inconsistencies:
            print(f'Inconsistencies found in booktitle for entry {self.name}.')
        return
