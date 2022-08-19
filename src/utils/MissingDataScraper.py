# Shree KRISHNAya Namaha
# Scrapes missing data for the existing entries from Google scholar
# Author: Nagabhushan S N
# Last Modified: 19/08/22
import copy
import json
import re
import sys
import time
import datetime
import traceback

from pathlib import Path
from tkinter import Tk

import pyautogui
from tqdm import tqdm

from data_structures.EntryCollection import EntryCollection
from data_structures.entry_types.Conference import ConferenceEntry
from data_structures.entry_types.Generic import GenericEntry
from data_structures.entry_types.Journal import JournalEntry

this_filepath = Path(__file__)
this_filename = this_filepath.stem


class MissingDataScraper:
    def __init__(self):
        pyautogui.PAUSE = 0.25
        pyautogui.FAILSAFE = True

        self.search_bar_location = (591, 76)
        self.search_field_location = (1008, 364)
        self.cite_location = (397, 351)
        self.bibtex_location = (895, 722)
        self.num_scrape_retries = 5

        self.tk = Tk()
        self.tk.withdraw()

        return

    def scrape_missing_data(self):
        pyautogui.hotkey('alt', 'tab')
        time.sleep(5)

        entry_collection = EntryCollection()
        bib_data = entry_collection.entries
        updated_bib_data = []
        progress_bar = tqdm(bib_data)
        for bib_entry in progress_bar:
            progress_bar.set_description(bib_entry.name)
            updated_bib_entry = self.scrape_bib_entry(bib_entry)
            updated_bib_data.append(updated_bib_entry)
            entry_collection.entries = updated_bib_data
            entry_collection.save_to_disk()
        pyautogui.hotkey('alt', 'tab')
        return

    def scrape_bib_entry(self, bib_entry: GenericEntry):
        match bib_entry.__class__.__qualname__:
            case JournalEntry.__qualname__:
                updated_bib_entry = self.scrape_journal_entry(bib_entry)

            case ConferenceEntry.__qualname__:
                updated_bib_entry = self.scrape_conference_entry(bib_entry)

            case _:
                updated_bib_entry = copy.copy(bib_entry)
        return updated_bib_entry

    def scrape_journal_entry(self, journal_entry: JournalEntry):
        updated_journal_entry = copy.copy(journal_entry)
        if (journal_entry.journal_full is None) and (journal_entry.journal_short is None):
            return updated_journal_entry

        scraping_required = any(map(lambda x: x is None, [journal_entry.volume, journal_entry.number, journal_entry.pages, journal_entry.year, journal_entry.month, journal_entry.doi, journal_entry.organization]))
        if not scraping_required:
            return updated_journal_entry

        scraped_bib_data = self.scrape_from_google_scholar(journal_entry.title)
        self.update_entry(updated_journal_entry.__dict__, scraped_bib_data, ['volume', 'number', 'pages', 'year', 'month', 'doi', 'organization'])
        return updated_journal_entry

    def scrape_conference_entry(self, conference_entry: ConferenceEntry):
        updated_conference_entry = copy.copy(conference_entry)
        if (conference_entry.booktitle_full is None) and (conference_entry.booktitle_short is None):
            return updated_conference_entry

        scraping_required = any(map(lambda x: x is None, [conference_entry.volume, conference_entry.pages, conference_entry.year, conference_entry.month, conference_entry.doi, conference_entry.organization]))
        if not scraping_required:
            return updated_conference_entry

        scraped_bib_data = self.scrape_from_google_scholar(conference_entry.title)
        self.update_entry(updated_conference_entry.__dict__, scraped_bib_data, ['volume', 'pages', 'year', 'month', 'doi', 'organization'])
        return updated_conference_entry

    def scrape_from_google_scholar(self, title):
        parsed_bib_data = None
        i = 0

        while (parsed_bib_data is None) and (i < self.num_scrape_retries):
            pyautogui.hotkey('ctrl', 't')  # Open a new tab
            pyautogui.click(*self.search_bar_location)
            pyautogui.typewrite('scholar.google.com')
            pyautogui.press('enter')
            time.sleep(5)

            pyautogui.click(*self.search_field_location)
            pyautogui.typewrite(title)
            pyautogui.press('enter')
            time.sleep(5)

            pyautogui.hotkey('ctrl', 'f')
            pyautogui.typewrite('cite')
            pyautogui.hotkey('ctrl', 'enter')
            # pyautogui.click(*self.cite_location)
            time.sleep(2)

            pyautogui.hotkey('ctrl', 'f')
            pyautogui.typewrite('bibtex')
            pyautogui.hotkey('ctrl', 'enter')
            # pyautogui.click(*self.bibtex_location)
            time.sleep(5)

            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            raw_bib_data = self.tk.clipboard_get()
            parsed_bib_data = self.parse_scraped_google_scholar_bib_data(raw_bib_data)

            pyautogui.hotkey('ctrl', 'w')  # close the opened tab
            i += 1
        return parsed_bib_data

    @staticmethod
    def parse_scraped_google_scholar_bib_data(raw_data: str):
        try:
            lines = raw_data.split('\n')[1:-1]
            if len(lines) > 2:
                parsed_data = {}
                for line in lines:
                    stripped_line = line.strip().rstrip(',')
                    key, value = re.match(r'(\w+)={([\s\S]+)}', stripped_line).groups()
                    parsed_data[key] = value
            else:
                parsed_data = None
        except AttributeError:
            parsed_data = None
        return parsed_data

    @staticmethod
    def update_entry(old_entry: dict, new_entry: dict, params):
        if new_entry is None:
            print(f'Parsing failed for {old_entry["name"]}')
            return

        warning_required = False
        inconsistencies = []
        for param in params:
            if param in new_entry:
                if old_entry[param] is None:
                    old_entry[param] = new_entry[param]
                elif old_entry[param] != new_entry[param]:
                    warning_required = True
                    inconsistencies.append((old_entry[param], new_entry[param]))
        if warning_required:
            warning_message = f'Inconsistencies found in {old_entry["name"]}: ' + str(inconsistencies)
            print(warning_message)
        return


def demo1():
    MissingDataScraper().scrape_missing_data()
    return


def main():
    demo1()
    return


if __name__ == '__main__':
    print('Program started at ' + datetime.datetime.now().strftime('%d/%m/%Y %I:%M:%S %p'))
    start_time = time.time()
    try:
        main()
        run_result = 'Program completed successfully!'
    except Exception as e:
        print(e)
        traceback.print_exc()
        run_result = 'Error: ' + str(e)
    end_time = time.time()
    print('Program ended at ' + datetime.datetime.now().strftime('%d/%m/%Y %I:%M:%S %p'))
    print('Execution time: ' + str(datetime.timedelta(seconds=end_time - start_time)))
