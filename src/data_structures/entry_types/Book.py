# Shree KRISHNAya Namaha
# Book
# Author: Nagabhushan S N
# Last Modified: 26-04-2020

import dataclasses
from dataclasses import dataclass
from typing import List

from data_structures.entry_types.Generic import GenericEntry
from utils import MonthUtils


@dataclass(eq=False)
class BookEntry(GenericEntry):
    volume: str = None
    publisher: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = BookEntry.extract_comment(raw_data)
        name = BookEntry.extract_name(raw_data)
        fields_dict = BookEntry.extract_fields(raw_data)
        book_entry = BookEntry(name=name)
        book_entry.comment = comment
        book_entry.title = fields_dict.get('title', None)
        book_entry.author = fields_dict.get('author', None)
        book_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        book_entry.year = fields_dict.get('year', None)
        book_entry.volume = fields_dict.get('volume', None)
        book_entry.publisher = fields_dict.get('publisher', None)
        book_entry.doi = fields_dict.get('doi', None)
        return book_entry

    def get_export_string(self, fields_names: list):
        lines = []
        if self.comment:
            lines.append(f'% {self.comment}')

        fields_dict = dataclasses.asdict(self)
        entry_name = fields_dict['name']
        lines.append(f'@book{{{entry_name},')

        if ('title' in fields_names) and self.title:
            lines.append(f'    title = {{{self.title}}},')
        if ('author' in fields_names) and self.author:
            lines.append(f'    author = {{{self.author}}},')
        if ('volume' in fields_names) and self.volume:
            lines.append(f'    volume = {{{self.volume}}},')
        if ('publisher' in fields_names) and self.publisher:
            lines.append(f'    publisher = {{{self.publisher}}},')
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
