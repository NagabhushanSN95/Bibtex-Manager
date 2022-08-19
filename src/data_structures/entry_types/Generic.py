# Shree KRISHNAya Namaha
# Generic Entry
# Author: Nagabhushan S N
# Last Modified: 25-04-2020

import abc
import dataclasses
import re
from dataclasses import dataclass
from typing import List

from utils import MonthUtils

BIB_FIELD_PATTERN = r'(\w+?) *?= *?{(.+)},?'
BIB_ENTRY_NAME_PATTERN = r'@\w+{(.+),'


@dataclass
class GenericEntry:
    name: str
    class_name: str = None
    comment: str = None
    title: str = None
    author: str = None
    month: str = None
    year: str = None
    doi: str = None

    def __post_init__(self):
        self.class_name = self.__class__.__name__

    @classmethod
    def from_dict(cls, data_dict: dict):
        return cls(**data_dict)

    def update(self, new_entry):
        new_entry_dict = dataclasses.asdict(new_entry)
        for key, value in new_entry_dict.items():
            if hasattr(self, key) and value:
                setattr(self, key, value)
        return

    @staticmethod
    def parse_raw_data(raw_data: List[str]):
        raise NotImplementedError

    @staticmethod
    def extract_comment(raw_data: List[str]):
        comment_lines = []
        for line in raw_data:
            if line.strip().startswith('%'):
                comment_lines.append(line.strip()[1:].strip())  # Removes leading %
            else:
                break
        comment = ';'.join(comment_lines)
        return comment

    @staticmethod
    def extract_name(raw_data: List[str]):
        name = None
        for line in raw_data:
            line1 = line.strip()
            if line1.startswith('%'):
                continue
            else:
                matcher = re.match(BIB_ENTRY_NAME_PATTERN, line1)
                if matcher:
                    name = matcher.group(1)
                else:
                    print(f'Error: Unable to extract name from "{line1}"')
                break
        return name

    @staticmethod
    def extract_fields(raw_data: List[str]):
        fields_dict = {}
        for line in raw_data:
            line1 = line.strip()
            if line1.startswith('%') or line1.startswith('@'):
                continue
            elif line1.startswith('}'):
                break
            else:
                matcher = re.match(BIB_FIELD_PATTERN, line1)
                if matcher:
                    field_name = matcher.group(1).lower()
                    field_value = matcher.group(2)
                    fields_dict[field_name] = field_value
                else:
                    print(f'Warning: Unable to parse "{line1}"')
        return fields_dict

    def compose_month(self, fields_names1: list):
        month = None
        if self.month is not None:
            if 'month' in fields_names1:
                month = self.month
            elif 'month_short' in fields_names1:
                month = MonthUtils.month_long_to_short(self.month)
        return month

    @abc.abstractmethod
    def get_export_string(self, fields_names: list):
        return NotImplementedError

    def fill_missing_data(self):
        return

    def check_inconsistencies(self):
        return

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        name_pattern = r'^(\w+?)(\d{4})(\w+?)$'
        self_matcher = re.match(name_pattern, self.name)
        self_reordered_name = f'{self_matcher.group(2)}_{self_matcher.group(1)}_{self_matcher.group(3)}'
        other_matcher = re.match(name_pattern, other.name)
        other_reordered_name = f'{other_matcher.group(2)}_{other_matcher.group(1)}_{other_matcher.group(3)}'
        return self_reordered_name < other_reordered_name
