# Building Configs

Config files are nothing but json data.
Config files list out what all fields have to be included in each entry type, while exporting bib file.
They must include all entry types available.
The output bib filename is the same as that of config filename

Currently, the below are available/supported

* Conference Entry
    * title
    * author
    * booktitle_full/booktitle_short
    * booktitle_abbreviation
    * month
    * year
* Journal Entry
    * title
    * author
    * journal_full/journal_short
    * journal_abbreviation
    * volume
    * number
    * pages
    * month
    * year
* arXiv Entry
    * title
    * author
    * journal
    * eid
    * pages
    * archivePrefix
    * eprint
    * month
    * year
* bioRxiv Entry
    * title
    * author
    * journal
    * eid
    * month
    * year
* TechReport Entry
    * title
    * author
    * institution_full/institution_short
    * month
    * year
* Book Entry
    * title
    * author
    * volume
    * month
    * year
* Misc Entry
    * title
    * author
    * year
    * url