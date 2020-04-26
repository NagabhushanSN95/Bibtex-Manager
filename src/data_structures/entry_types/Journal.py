# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

import dataclasses
import re
from dataclasses import dataclass
from typing import List

from src.data_structures.entry_types.Generic import GenericEntry

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
        journal_entry.month = fields_dict.get('month', None)
        journal_entry.year = fields_dict.get('year', None)
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
        else:
            return None
        if 'journal_abbreviation' in fields_names1 and self.journal_abbreviation:
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
        if self.compose_journal(fields_names):
            lines.append(f'    journal = {{{self.compose_journal(fields_names)}}},')
        if ('volume' in fields_names) and self.volume:
            lines.append(f'    volume = {{{self.volume}}},')
        if ('number' in fields_names) and self.number:
            lines.append(f'    number = {{{self.number}}},')
        if ('pages' in fields_names) and self.pages:
            lines.append(f'    pages = {{{self.pages}}},')
        if ('month' in fields_names) and self.month:
            lines.append(f'    month = {{{self.month}}}')
        if ('year' in fields_names) and self.year:
            lines.append(f'    year = {{{self.year}}}')
        lines.append('}')
        export_string = '\n'.join(lines)
        return export_string
