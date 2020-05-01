# Conventions

1. General rule is to have as little information as possible, with which the article can be accurately searched in web.
2. If a transaction paper follows the conference paper, cite transaction paper only
3. If there is a conflict between Google Scholar bibtex and IEEE/ACM bibtex, prefer IEEE/ACM bibtex.
4. Sort the entries alphabetical order of their names (number comes before any letters)
5. For the name of an entry
    1. follow google scholar convention: last name of the first author, year, first word of the title (except common words)
6. For titles
    1. keep the title name exactly as it appeared in the paper (caps and others), even though bibtex might convert them to lowercase
    2. for abbreviations like GAN, include them in braces {GAN}, so that bibtex will leave it capitalized
7. For author names
    1. format: last-name, first-name middle-initial
    2. if it has special characters, include them: Example Doll\'ar
8. For booktitle/journal,
    1. if abbreviation is famous, include that abbreviation in parenthesis, for conferences only
    2. do not include year (Reason: year will get repeated too many times)
    3. shortening of conference/journal name
        1. for conference: do not shorten
        2. for journal: shorten
    4. include "proceedings" word only if the conference official name says that.
9. volume/number/pages:
    1. include for journals, exclude for conferences
10. Don't include organization/publisher
11. For arXiv references, write as follows:
    ```
    journal = {arXiv e-prints},
    eid = {arXiv:1804.01523},
    pages = {arXiv:1804.01523},
    archivePrefix = {arXiv},
    eprint = {1804.01523},
    ```
12. Comments:
    1. Above the bibtex entry, include a short name for the paper, if that name is famous.