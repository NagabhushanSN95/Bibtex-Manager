# Shree KRISHNAya Namaha
# A collection of entries. An object of this class stores complete data
# Author: Nagabhushan S N
# Last Modified: 25-04-2020
import json
import dataclasses
from dataclasses import dataclass
from typing import List

from pathlib import Path

from src.data_structures.entry_types.EntryFactory import EntryFactory
from src.data_structures.entry_types.Generic import GenericEntry


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
            json.dump(data_dict, data_file)
        return

    def add_entry(self, entry: GenericEntry):
        if any(entry == entry1 for entry1 in self.entries):
            existing_entry = next(entry1 for entry1 in self.entries if entry == entry1)
            existing_entry.update(entry)
        else:
            self.entries.append(entry)

    def sort(self):
        self.entries = sorted(self.entries)
        return
