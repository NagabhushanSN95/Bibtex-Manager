# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 26-04-2020

import dataclasses
import re
from dataclasses import dataclass
from typing import List

from src.data_structures.entry_types.Generic import GenericEntry


@dataclass(eq=False)
class TechReportEntry(GenericEntry):
    institution_full: str = None
    institution_short: str = None

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        comment = TechReportEntry.extract_comment(raw_data)
        name = TechReportEntry.extract_name(raw_data)
        fields_dict = TechReportEntry.extract_fields(raw_data)
        tech_report_entry = TechReportEntry(name=name)
        tech_report_entry.comment = comment
        tech_report_entry.title = fields_dict.get('title', None)
        tech_report_entry.author = fields_dict.get('author', None)
        tech_report_entry.month = fields_dict.get('month', None)
        tech_report_entry.year = fields_dict.get('year', None)

        institution_data = TechReportEntry.parse_institution(fields_dict.get('institution', None))
        tech_report_entry.institution_full = institution_data[0]
        tech_report_entry.institution_short = institution_data[1]
        return tech_report_entry

    @staticmethod
    def parse_institution(institution: str):
        if not institution:
            full_name = None
            short_name = None
        else:
            short_forms = ['Int.']
            if any(short_form in institution.lower() for short_form in short_forms):
                short_name = institution
                full_name = None
            else:
                short_name = None
                full_name = institution
        return full_name, short_name

    def compose_institution(self, fields_names1: list):
        if 'institution_full' in fields_names1:
            if self.institution_full:
                institution = self.institution_full
            else:
                institution = self.institution_short
        elif 'institution_short' in fields_names1:
            if self.institution_short:
                institution = self.institution_short
            else:
                institution = self.institution_full
        else:
            return None
        return institution

    def get_export_string(self, fields_names: list):
        lines = []
        if self.comment:
            lines.append(f'% {self.comment}')

        fields_dict = dataclasses.asdict(self)
        entry_name = fields_dict['name']
        lines.append(f'@techreport{{{entry_name},')

        if ('title' in fields_names) and self.title:
            lines.append(f'    title = {{{self.title}}},')
        if ('author' in fields_names) and self.author:
            lines.append(f'    author = {{{self.author}}},')
        if self.compose_institution(fields_names):
            lines.append(f'    institution = {{{self.compose_institution(fields_names)}}},')
        if ('month' in fields_names) and self.month:
            lines.append(f'    month = {{{self.month}}}')
        if ('year' in fields_names) and self.year:
            lines.append(f'    year = {{{self.year}}}')
        lines.append('}')
        export_string = '\n'.join(lines)
        return export_string
