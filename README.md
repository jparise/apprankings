# App Store Rankings Scraper

Copyright &copy; 2011 Jon Parise &lt;jon@indelible.org&gt;

`apprankings.py` scrapes App Store rankings from iTunes and writes the results
to a CSV-formatted output file.  It currently queries both the iPhone and iPad
App Stores for the *Paid*, *Free*, and *Top Grossing* lists.  It covers the
*All* and *Games* categories, but it could be further extended and
parameterized to support a much wider range of queries.

This code is released under the terms of the [MIT License][license].

## Usage

    usage: apprankings.py [-h] [-a APPS [APPS ...]] [-c COUNTRIES [COUNTRIES ...]]
                        [-o OUTPUT] [-v]

    Scrape App Store rankings

    optional arguments:
    -h, --help            show this help message and exit
    -v, --verbose         verbose logging output
    -a APPS [APPS ...], --apps APPS [APPS ...]
                            include only these app IDs in the output
    -c COUNTRIES [COUNTRIES ...], --countries COUNTRIES [COUNTRIES ...]
                            list of ISO-3166-1 Alpha-2 country codes to query
    -o OUTPUT, --output OUTPUT
                            CSV-formatted output file (default: rankings.csv)

## TODO

* Support for parametizable category queries.
* Consider adding more output fields:
  * Developer
  * Link
  * Price
  * Updated Date
* Profile for performance improvements

[license]: http://www.opensource.org/licenses/mit-license.php
