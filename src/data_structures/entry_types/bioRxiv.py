# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

import dataclasses
from dataclasses import dataclass
from typing import List

from data_structures.entry_types.Generic import GenericEntry
from utils import MonthUtils


@dataclass(eq=False)
class bioRxivEntry(GenericEntry):
    journal: str = "bioRxiv"
    eid: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = bioRxivEntry.extract_comment(raw_data)
        name = bioRxivEntry.extract_name(raw_data)
        fields_dict = bioRxivEntry.extract_fields(raw_data)
        arxiv_entry = bioRxivEntry(name=name)
        arxiv_entry.comment = comment
        arxiv_entry.title = fields_dict.get('title', None)
        arxiv_entry.author = fields_dict.get('author', None)
        arxiv_entry.eid = fields_dict.get('eid', None)
        arxiv_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        arxiv_entry.year = fields_dict.get('year', None)
        arxiv_entry.doi = fields_dict.get('doi', None)
        return arxiv_entry

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
        if ('journal' in fields_names) and self.journal:
            lines.append(f'    journal = {{{self.journal}}},')
        if ('eid' in fields_names) and self.eid:
            lines.append(f'    eid = {{{self.eid}}},')
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
