# 08 Bibtex Manager

To manage references bib files.

## Features:
1. Automatic export of bib files in with configurable formats
2. Automagic infilling of full_name/short_name/abbreviation of journal/conference titles [More Info](res/short_forms/ReadMe.md)
3. Automatic sorting of entries according to year [Convention](./res/configs/Conventions.md)
4. Warnings to inconsistencies in journal/conference names [More Info](res/short_forms/ReadMe.md)
5. Warnings to duplicate entries with just a change in year


## Conventions:
Conventions followed are listed [here](./res/configs/Conventions.md).

## How to use:
### Importing existing bib files:
Run `src/BibtexParser.py` by passing the path to the bib file.

### Exporting bib files:
1. Create a config file indicating the fields to include in the bib file.
There are a few examples in `res/configs/`. Refer to [Configs ReadMe](./res/configs/ReadMe.md).
2. Run `src/BibtexExporter.py` by passing the path to the config file.
Output bib file will be stored  `out/` directory with name `references_{config_filename}.bib`

## BIB entry types supported:
* Conference Entry (@inproceedings)
    * title
    * author
    * booktitle (full/short + abbreviation)
    * month
    * year
* Conference Workshop Entry
    * title
    * author
    * booktitle (conference name full/short + abbreviation + workshop name full/short + abbreviation)
    * month
    * year
* Journal Entry (@article)
    * title
    * author
    * journal (full/short + abbreviation)
    * volume
    * number
    * pages
    * month
    * year
* arXiv Entry (@article)
    * title
    * author
    * journal
    * eid
    * pages
    * archivePrefix
    * eprint
    * month
    * year
* bioRxiv Entry (@article)
    * title
    * author
    * journal
    * eid
    * month
    * year
* TechReport Entry (@techreport)
    * title
    * author
    * institution_full/institution_short
    * month
    * year
* Book Entry (@book)
    * title
    * author
    * volume
    * month
    * year
* Misc Entry (@misc)
    * title
    * author
    * year
    * url

## GUI
Coming Soon

## Disclaimer
**TL;DR;**  
Fork this repository and use this tool in conjunction with git.

**Detail Explanation**  
This is still Work In Progress (WIP).
So there might be a lot of inadvertent bugs.
In order to not lose out any information, fork this repository and push any changes you make to your repo.
Always cross-check once before pushing updates to the repo.
That way, any inadvertent changes can be easily caught.

## Bug Reports / Feature Request
Please raise an issue to report any bugs or to request any new features or for any other help.
