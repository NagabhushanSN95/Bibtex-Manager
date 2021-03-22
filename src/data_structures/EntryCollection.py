# Shree KRISHNAya Namaha
# A collection of entries. An object of this class stores complete data
# Author: Nagabhushan S N
# Last Modified: 26-04-2020

import dataclasses
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from data_structures.entry_types.EntryFactory import EntryFactory
from data_structures.entry_types.Generic import GenericEntry
import simplejson


@dataclass()
class EntryCollection:
    entries: List[GenericEntry]

    def __init__(self):
        self.datastore_path = Path('../Data/ModelData/Data.json')
        self.entries = []
        self.load_from_disk()

    def load_from_disk(self):
        if not self.datastore_path.exists():
            return
        with open(self.datastore_path.as_posix(), 'r') as data_file:
            data = json.load(data_file)
        for json_entry in data['entries']:
            if json_entry:
                entry = EntryFactory.dict2entry(json_entry)
                self.add_entry(entry)
            else:
                print('Warning! Encountered None entry while reading data from disk')
        return

    def save_to_disk(self):
        if not self.datastore_path.parent.exists():
            self.datastore_path.parent.mkdir(parents=True)
        data_dict = dataclasses.asdict(self)
        with open(self.datastore_path.as_posix(), 'w') as data_file:
            simplejson.dump(data_dict, data_file, indent=4)
        return

    def add_entry(self, entry: GenericEntry):
        if any(entry == entry1 for entry1 in self.entries):
            existing_entry = next(entry1 for entry1 in self.entries if entry == entry1)
            existing_entry.update(entry)
        else:
            self.entries.append(entry)

    def refresh(self):
        self.sort()
        self.fill_short_forms()
        self.check_inconsistencies()
        self.check_duplicates()
        return

    def sort(self):
        self.entries = sorted(self.entries)
        return

    def fill_short_forms(self):
        for entry in self.entries:
            entry.fill_missing_data()
        return

    def check_inconsistencies(self):
        for entry in self.entries:
            entry.check_inconsistencies()
        return

    def check_duplicates(self):
        name_sans_year_list = []
        name_pattern = r'^(\w+?)(\d{4})(\w+?)$'
        for entry in self.entries:
            matcher = re.match(name_pattern, entry.name)
            name_sans_year = f'{matcher.group(1)}_{matcher.group(3)}'
            if name_sans_year in name_sans_year_list:
                matching_index = name_sans_year_list.index(name_sans_year)
                print(f'Warning: Possible duplicate entries: {self.entries[matching_index].name} and {entry.name}')
            else:
                name_sans_year_list.append(name_sans_year)
        return
