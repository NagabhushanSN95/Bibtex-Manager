# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

import dataclasses
import re
from dataclasses import dataclass
from typing import List

from data_structures.entry_types.Generic import GenericEntry
from utils import MonthUtils

EID_PATTERN = r'.+arXiv:(\d+.\d+)$'


@dataclass(eq=False)
class arXivEntry(GenericEntry):
    journal: str = "arXiv e-prints"
    eid: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = arXivEntry.extract_comment(raw_data)
        name = arXivEntry.extract_name(raw_data)
        fields_dict = arXivEntry.extract_fields(raw_data)
        arxiv_entry = arXivEntry(name=name)
        arxiv_entry.comment = comment
        arxiv_entry.title = fields_dict.get('title', None)
        arxiv_entry.author = fields_dict.get('author', None)
        arxiv_entry.eid = arXivEntry.parse_eid(fields_dict.get('eid', None))
        if arxiv_entry.eid is None:
            arxiv_entry.eid = arXivEntry.parse_eid(fields_dict.get('pages', None))
        if arxiv_entry.eid is None:
            arxiv_entry.eid = arXivEntry.parse_eid(fields_dict.get('journal', None))
        arxiv_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        arxiv_entry.year = fields_dict.get('year', None)
        arxiv_entry.doi = fields_dict.get('doi', None)
        return arxiv_entry

    @staticmethod
    def parse_eid(eid_str: str):
        eid = None
        if eid_str:
            matcher = re.match(EID_PATTERN, eid_str)
            if matcher:
                eid = matcher.group(1)
        return eid

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
            lines.append(f'    eid = {{arXiv:{self.eid}}},')
        if ('pages' in fields_names) and self.eid:
            lines.append(f'    pages = {{arXiv:{self.eid}}},')
        if ('url' in fields_names) and self.eid:
            lines.append(f'    url = {{arXiv:{self.eid}}},')
        if 'archivePrefix' in fields_names:
            lines.append(f'    archivePrefix = {{arXiv}},')
        if ('eprint' in fields_names) and self.eid:
            lines.append(f'    eprint = {{{self.eid}}},')
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
