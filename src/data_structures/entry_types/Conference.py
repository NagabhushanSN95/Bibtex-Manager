# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

import dataclasses
import re
from dataclasses import dataclass
from typing import List

from src.data_structures.entry_types.Generic import GenericEntry

BOOKTITLE_ABBREVIATION_PATTERN = r'(.+?) \((\w+)\)$'


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
        conf_entry.month = fields_dict.get('month', None)
        conf_entry.year = fields_dict.get('year', None)
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
        elif 'booktitle_short' in fields_names1:
            if self.booktitle_short:
                booktitle = self.booktitle_short
            else:
                booktitle = self.booktitle_full
        else:
            return None
        if 'booktitle_abbreviation' in fields_names1 and self.booktitle_abbreviation:
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
        if ('month' in fields_names) and self.month:
            lines.append(f'    month = {{{self.month}}}')
        if ('year' in fields_names) and self.year:
            lines.append(f'    year = {{{self.year}}}')
        lines.append('}')
        export_string = '\n'.join(lines)
        return export_string
