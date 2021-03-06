# Shree KRISHNAya Namaha
# Book
# Author: Nagabhushan S N
# Last Modified: 26-04-2020

import dataclasses
from dataclasses import dataclass
from typing import List

from data_structures.entry_types.Generic import GenericEntry


@dataclass(eq=False)
class BookEntry(GenericEntry):
    volume: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = BookEntry.extract_comment(raw_data)
        name = BookEntry.extract_name(raw_data)
        fields_dict = BookEntry.extract_fields(raw_data)
        book_entry = BookEntry(name=name)
        book_entry.comment = comment
        book_entry.title = fields_dict.get('title', None)
        book_entry.author = fields_dict.get('author', None)
        book_entry.month = fields_dict.get('month', None)
        book_entry.year = fields_dict.get('year', None)
        book_entry.volume = fields_dict.get('volume', None)
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
        if ('month' in fields_names) and self.month:
            lines.append(f'    month = {{{self.month}}}')
        if ('year' in fields_names) and self.year:
            lines.append(f'    year = {{{self.year}}}')
        lines.append('}')
        export_string = '\n'.join(lines)
        return export_string
