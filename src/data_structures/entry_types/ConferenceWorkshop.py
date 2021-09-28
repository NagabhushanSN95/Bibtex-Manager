# Shree KRISHNAya Namaha
# Conference Workshop paper
# Author: Nagabhushan S N
# Last Modified: 27-04-2020

import ast
import dataclasses
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from data_structures.entry_types.Generic import GenericEntry

BOOKTITLE_PATTERN1 = r'(.+?)( \(\w+\))? workshop on (.+?)( \(\w+\))?$'
BOOKTITLE_PATTERN2 = r'(.+?)( \(\w+\))? Workshops$'


@dataclass(eq=False)
class ConferenceWorkshopEntry(GenericEntry):
    booktitle_full: str = None
    booktitle_short: str = None
    booktitle_abbreviation: str = None
    workshop_full: str = None
    workshop_short: str = None
    workshop_abbreviation: str = None
    organization: str = None
    pages: str = None
    volume: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = ConferenceWorkshopEntry.extract_comment(raw_data)
        name = ConferenceWorkshopEntry.extract_name(raw_data)
        fields_dict = ConferenceWorkshopEntry.extract_fields(raw_data)
        conf_entry = ConferenceWorkshopEntry(name=name)
        conf_entry.comment = comment
        conf_entry.title = fields_dict.get('title', None)
        conf_entry.author = fields_dict.get('author', None)
        conf_entry.month = fields_dict.get('month', None)
        conf_entry.year = fields_dict.get('year', None)
        conf_entry.organization = fields_dict.get('organization', None)
        conf_entry.pages = fields_dict.get('pages', None)
        conf_entry.volume = fields_dict.get('volume', None)

        booktitle_data = ConferenceWorkshopEntry.parse_booktitle(fields_dict.get('booktitle', None))
        conf_entry.booktitle_full = booktitle_data[0]
        conf_entry.booktitle_short = booktitle_data[1]
        conf_entry.booktitle_abbreviation = booktitle_data[2]
        conf_entry.workshop_full = booktitle_data[3]
        conf_entry.workshop_short = booktitle_data[4]
        conf_entry.workshop_abbreviation = booktitle_data[5]
        return conf_entry

    @staticmethod
    def parse_booktitle(booktitle: str):
        conf_full_name = None
        conf_short_name = None
        conf_abbreviation = None
        captured_conf_name = None
        ws_full_name = None
        ws_short_name = None
        ws_abbreviation = None
        captured_ws_name = None
        if booktitle:
            matcher1 = re.match(BOOKTITLE_PATTERN1, booktitle)
            matcher2 = re.match(BOOKTITLE_PATTERN2, booktitle)
            if matcher1:
                captured_conf_name = matcher1.group(1)
                conf_abbreviation = matcher1.group(2)[2:-1]
                captured_ws_name = matcher1.group(3)
                ws_abbreviation = matcher1.group(4)
            elif matcher2:
                captured_conf_name = matcher2.group(1)
                conf_abbreviation = matcher2.group(2)
                if conf_abbreviation is not None:
                    conf_abbreviation = conf_abbreviation[2:-1]

            if captured_conf_name:
                conf_short_forms = ['conf.']
                if any(short_form in captured_conf_name.lower() for short_form in conf_short_forms):
                    conf_short_name = captured_conf_name
                    conf_full_name = None
                else:
                    conf_short_name = None
                    conf_full_name = captured_conf_name

            if captured_ws_name:
                ws_short_forms = ['ws.']
                if any(short_form in captured_ws_name.lower() for short_form in ws_short_forms):
                    ws_short_name = captured_ws_name
                    ws_full_name = None
                else:
                    ws_short_name = None
                    ws_full_name = captured_ws_name

        return conf_full_name, conf_short_name, conf_abbreviation, ws_full_name, ws_short_name, ws_abbreviation

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
        elif 'booktitle_abbreviation' in fields_names1:
            if self.booktitle_abbreviation is None:
                booktitle = self.booktitle_full
            else:
                booktitle = self.booktitle_abbreviation
        else:
            return None
        if 'booktitle_abbreviation' in fields_names1 and self.booktitle_abbreviation:
            if ('booktitle_full' in fields_names1) or ('booktitle_short' in fields_names1):
                # This branch handles the case when short+abbr or full+abbr is used. Just abbr is handled in previous
                # branch
                booktitle += f' ({self.booktitle_abbreviation})'

        if 'workshop_full' in fields_names1:
            if self.workshop_full:
                workshop = self.workshop_full
            else:
                workshop = self.workshop_short
        elif 'workshop_short' in fields_names1:
            if self.workshop_short:
                workshop = self.workshop_short
            else:
                workshop = self.workshop_full
        else:
            workshop = ''
        if 'workshop_abbreviation' in fields_names1 and self.workshop_abbreviation:
            if workshop:
                workshop += f' ({self.workshop_abbreviation})'
            else:
                workshop += f'{self.workshop_abbreviation}'

        if 'workshop_full' in fields_names1:
            workshop_text = 'Workshop'
        elif 'workshop_short' in fields_names1:
            workshop_text = 'Worksh.'
        else:
            workshop_text = ''

        if workshop is not None:
            complete_booktitle = booktitle + " " + workshop_text + " on " + workshop
        else:
            complete_booktitle = booktitle + " " + workshop_text
        return complete_booktitle

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

        # TODO: Do the same for workshop part
        return

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

        # TODO: Do the same for workshop part
        return
