# Shree KRISHNAya Namaha
# Conference paper
# Author: Nagabhushan S N
# Last Modified: 26-04-2020

import ast
import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import List

from data_structures.entry_types.Generic import GenericEntry
from utils import MonthUtils


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
        tech_report_entry.month = MonthUtils.month_to_long(fields_dict.get('month', None))
        tech_report_entry.year = fields_dict.get('year', None)
        tech_report_entry.doi = fields_dict.get('doi', None)

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
        self.fill_institution_names()

    def fill_institution_names(self):
        institutions_data = self.get_institutions_data()

        if not self.institution_full:
            if self.institution_short:
                institution_data = self.get_matching_institution_data(institutions_data, self.institution_short, index=1)
            else:
                institution_data = None
            if institution_data and institution_data[0]:
                self.institution_full = institution_data[0]

        if not self.institution_short:
            if self.institution_full:
                institution_data = self.get_matching_institution_data(institutions_data, self.institution_full, index=0)
            else:
                institution_data = None
            if institution_data and institution_data[1]:
                self.institution_short = institution_data[1]

    @staticmethod
    def get_institutions_data():
        institution_data_path = Path('../res/short_forms/institutions.txt')
        with open(institution_data_path.as_posix(), 'r') as institution_file:
            lines = institution_file.readlines()
        institutions_data = [ast.literal_eval(line.strip()) for line in lines]
        return institutions_data

    @staticmethod
    def get_matching_institution_data(institutions_data: List[tuple], search_str: str, index: int):
        for institution_data in institutions_data:
            if institution_data[index] == search_str:
                return institution_data
        return None

    def check_inconsistencies(self):
        self.check_institution_inconsistencies()

    def check_institution_inconsistencies(self):
        def match_institution(institution_data1: tuple):
            if institution_data1:
                if (institution_data1[0] and (self.institution_full != institution_data1[0])) or \
                        (institution_data1[1] and (self.institution_short != institution_data1[1])):
                    return True
            return False

        institutions_data = self.get_institutions_data()
        inconsistencies = False
        if self.institution_full:
            institution_data = self.get_matching_institution_data(institutions_data, self.institution_full, index=0)
            inconsistencies = inconsistencies or match_institution(institution_data)
        if self.institution_short:
            institution_data = self.get_matching_institution_data(institutions_data, self.institution_short, index=1)
            inconsistencies = inconsistencies or match_institution(institution_data)

        if inconsistencies:
            print(f'Inconsistencies found in institution for entry {self.name}.')
        return
