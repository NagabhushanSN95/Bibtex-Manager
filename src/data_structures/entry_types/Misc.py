# Shree KRISHNAya Namaha
# Misc Entries
# Author: Nagabhushan S N
# Last Modified: 24-06-2021

import dataclasses
import re
from dataclasses import dataclass
from typing import List

from data_structures.entry_types.Generic import GenericEntry
from utils import MonthUtils


@dataclass(eq=False)
class MiscEntry(GenericEntry):
    journal: str = None
    url: str = None
    note: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = MiscEntry.extract_comment(raw_data)
        name = MiscEntry.extract_name(raw_data)
        fields_dict = MiscEntry.extract_fields(raw_data)
        book_entry = MiscEntry(name=name)
        book_entry.comment = comment
        book_entry.title = fields_dict.get('title', None)
        book_entry.author = fields_dict.get('author', None)
        book_entry.journal = fields_dict.get('journal', None)
        book_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        book_entry.year = fields_dict.get('year', None)
        book_entry.doi = fields_dict.get('doi', None)
        if fields_dict.get('howpublished', None) is not None:
            url = fields_dict.get('howpublished', None)
            matcher = re.match(r'^\\url{(.+)}$', url)
            if matcher is not None:
                url = matcher.group(1)
            book_entry.url = url
        else:
            book_entry.url = fields_dict.get('url', None)
        book_entry.note = fields_dict.get('note', None)
        return book_entry

    def get_export_string(self, fields_names: list):
        lines = []
        if self.comment:
            lines.append(f'% {self.comment}')

        fields_dict = dataclasses.asdict(self)
        entry_name = fields_dict['name']
        lines.append(f'@misc{{{entry_name},')

        if ('title' in fields_names) and self.title:
            lines.append(f'    title = {{{self.title}}},')
        if ('author' in fields_names) and self.author:
            lines.append(f'    author = {{{self.author}}},')
        if ('journal' in fields_names) and self.journal:
            lines.append(f'    journal = {{{self.journal}}},')
        if ('url' in fields_names) and self.url:
            lines.append(f'    howpublished = {{\\url{{{self.url}}}}},')
        if ('note' in fields_names) and self.note:
            lines.append(f'    note = {{{self.note}}},')
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
