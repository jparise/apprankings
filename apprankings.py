#!/usr/bin/env python
#
# App Store Rankings Scraper
# Jon Parise <jon@indelible.org>
#

import argparse
import csv
import datetime
import htmlentitydefs
import re
import sys
import urllib2

from collections import namedtuple

# App Store countries (keyed by ISO-3166-1 Alpha-2 code)
# We include each country's App Store-specific "store front" identifier.  This
# is required to get per-country query results.
Country = namedtuple('Country', ('name', 'storefront'))
countries = {
    'DZ': Country('Algeria', '143563,12'),
    'AO': Country('Angola',  '143564,12'),
    'AI': Country('Anguilla', '143538,12'),
    'AG': Country('Antigua and Barbuda', '143540,12'),
    'AR': Country('Argentina', '143505-2,12'),
    'AM': Country('Armenia', '143524,12'),
    'AU': Country('Australia', '143460,12'),
    'AZ': Country('Azerbaijan', '143568,12'),
    'BS': Country('Bahamas', '143539,12'),
    'BH': Country('Bahrain', '143559,12'),
    'BB': Country('Barbados', '143541,12'),
    'BY': Country('Belarus', '143565,12'),
    'BE': Country('Belgium', '143446-2,12'),
    'BZ': Country('Belize', '143555-2,12'),
    'BM': Country('Bermuda', '143542,12'),
    'BO': Country('Bolivia', '143556,12'),
    'BW': Country('Botswana', '143525,12'),
    'BR': Country('Brazil', '143503,12'),
    'VG': Country('British Virgin Islands', '143543,12'),
    'BN': Country('Brunei Darussalam', '143560,12'),
    'CA': Country('Canada', '143455-6,12'),
    'KY': Country('Cayman Islands', '143544,12'),
    'CZ': Country('Czech Republic', '143489,12'),
    'CL': Country('Chile', '143483-2,12'),
    'CO': Country('Colombia', '143501-2,12'),
    'CR': Country('Costa Rica', '143495-2,12'),
    'CY': Country('Cyprus', '143557-2,12'),
    'DK': Country('Denmark', '143458-2,12'),
    'DE': Country('Germany', '143443,12'),
    'DM': Country('Dominica', '143545,12'),
    'EC': Country('Ecuador', '143509-2,12'),
    'EE': Country('Estonia', '143518,12'),
    'EG': Country('Egypt', '143516,12'),
    'SV': Country('El Salvador', '143506-2,12'),
    'ES': Country('Spain', '143454-8,12'),
    'FR': Country('France', '143442,12'),
    'GH': Country('Ghana', '143573,12'),
    'GR': Country('Greece', '143448,12'),
    'GD': Country('Grenada', '143546,12'),
    'GT': Country('Guatemala', '143504-2,12'),
    'GY': Country('Guyana', '143553,12'),
    'HN': Country('Honduras', '143510-2,12'),
    'HK': Country('Hong Kong', '143463,12'),
    'HR': Country('Croatia', '143494,12'),
    'IS': Country('Iceland', '143558,12'),
    'IN': Country('India', '143467,12'),
    'ID': Country('Indonesia', '143476,12'),
    'IE': Country('Ireland', '143449,12'),
    'IL': Country('Israel', '143491,12'),
    'IT': Country('Italy', '143450,12'),
    'JM': Country('Jamaica', '143511,12'),
    'JO': Country('Jordan', '143528,12'),
    'KZ': Country('Kazakhstan', '143517,12'),
    'KE': Country('Kenya', '143529,12'),
    'KW': Country('Kuwait', '143493,12'),
    'LV': Country('Latvia', '143519,12'),
    'LB': Country('Lebanon', '143497,12'),
    'LT': Country('Lithunaia', '143520,12'),
    'LU': Country('Luxembourg', '143451-2,12'),
    'MO': Country('Macao', '143515,12'),
    'MK': Country('Macedonia', '143530,12'),
    'MG': Country('Madagascar', '143531,12'),
    'HU': Country('Hungary', '143482,12'),
    'MY': Country('Malaysia', '143473,12'),
    'ML': Country('Mali', '143532,12'),
    'MT': Country('Malta', '143521,12'),
    'MU': Country('Mauritius', '143533,12'),
    'MX': Country('Mexico', '143468,12'),
    'MD': Country('Moldova', '143523,12'),
    'MS': Country('Montserrat', '143547,12'),
    'ML': Country('Netherlands', '143452,12'),
    'NZ': Country('New Zealand', '143461,12'),
    'NI': Country('Nicaragua', '143512-2,12'),
    'NE': Country('Niger', '143534,12'),
    'NG': Country('Nigeria', '143561,12'),
    'NO': Country('Norway', '143457-2,12'),
    'OM': Country('Oman', '143562,12'),
    'AT': Country('Austria', '143445,12'),
    'PK': Country('Pakistan', '143477,12'),
    'PA': Country('Panama', '143485-2,12'),
    'PY': Country('Paraguay', '143513-2,12'),
    'PE': Country('Peru', '143507-2,12'),
    'PH': Country('Philippines', '143474,12'),
    'PL': Country('Poland', '143478,12'),
    'PT': Country('Portugal', '143453,12'),
    'QA': Country('Qatar', '143498,12'),
    'DO': Country('Dominican Republic', '143508-2,12'),
    'RO': Country('Romania', '143487,12'),
    'SA': Country('Saudi Arabia', '143479,12'),
    'CH': Country('Switzerland', '143459-2,12'),
    'SN': Country('Senegal', '143535,12'),
    'SG': Country('Singapore', '143464,12'),
    'SK': Country('Slovakia', '143496,12'),
    'SI': Country('Slovenia', '143499,12'),
    'ZA': Country('South Africa', '143472,12'),
    'LK': Country('Sri Lanka', '143486,12'),
    'KN': Country('Saint Kitts and Nevis', '143548,12'),
    'LC': Country('Saint Lucia', '143549,12'),
    'VC': Country('Saint Vincent and the Grenadines', '143550,12'),
    'FI': Country('Finland', '143447-2,12'),
    'SR': Country('Suriname', '143554-2,12'),
    'SE': Country('Sweden', '143456,12'),
    'TZ': Country('Tanzania', '143572,12'),
    'TH': Country('Thailand', '143475,12'),
    'TT': Country('Trinidad and Tobago', '143551,12'),
    'TN': Country('Tunisia', '143536,12'),
    'TR': Country('Turkey', '143480,12'),
    'TC': Country('Turks and Caicos Islands', '143552,12'),
    'UG': Country('Uganda', '143537,12'),
    'GB': Country('United Kingdom', '143444,12'),
    'AE': Country('United Arab Emirates', '143481,12'),
    'US': Country('United States', '143441-1,12'),
    'UY': Country('Uruguay', '143514-2,12'),
    'UZ': Country('Uzbekistan', '143566,12'),
    'VE': Country('Venezuela', '143502-2,12'),
    'VN': Country('Viet Nam', '143471,12'),
    'YE': Country('Yemen', '143571,12'),
    'BG': Country('Bulgaria', '143526,12'),
    'RU': Country('Russian Federation', '143469,12'),
    'CN': Country('China', '143465-2,12'),
    'TW': Country('Taiwan', '143470,12'),
    'JP': Country('Japan', '143462-1,12'),
    'KR': Country('South Korea', '143466,12'),
}

store_url = 'http://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop'

queries = {
    ('iphone','all','paid'):      '?genreId=36&id=25129&popId=30',
    ('iphone','all','free'):      '?genreId=36&id=25129&popId=27',
    ('iphone','all','gross'):     '?genreId=36&id=25129&popId=38',
    ('ipad','all','paid'):        '?genreId=36&id=25129&popId=47',
    ('ipad','all','free'):        '?genreId=36&id=25129&popId=44',
    ('ipad','all','gross'):       '?genreId=36&id=25129&popId=46',
    ('iphone','games','paid'):    '?genreId=6014&id=25134&popId=30',
    ('iphone','games','free'):    '?genreId=6014&id=25134&popId=27',
    ('iphone','games','gross'):   '?genreId=6014&id=25134&popId=38',
    ('ipad','games','paid'):      '?genreId=6014&id=25134&popId=47',
    ('ipad','games','free'):      '?genreId=6014&id=25134&popId=44',
    ('ipad','games','gross'):     '?genreId=6014&id=25134&popId=46',
}

app_re = re.compile(r'<div.* aria-label="(.*)" adam-id="(\d+)"')
entities_re = re.compile(r'&(%s);' % '|'.join(htmlentitydefs.entitydefs))

def decode(text):
    """Decode HTML entities in the given text as a UTF-8 string."""
    # http://effbot.org/zone/re-sub.htm#unescape-html
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text).encode("utf-8")

def scrape(query, storefront):
    req = urllib2.Request(url=store_url + query)
    req.add_header('User-Agent', 'iTunes/10.4.1 (Macintosh; Intel Mac OS X 10.6.8) AppleWebKit/534.50')
    req.add_header('X-Apple-Store-Front', storefront)

    f = urllib2.urlopen(req)
    for rank, match in enumerate(app_re.finditer(f.read()), start=1):
        name, appid = match.groups()
        yield dict(rank=rank, name=decode(name), appid=int(appid))

def main(argv):
    # Handle argument parsing.
    parser = argparse.ArgumentParser(description='Scrape App Store rankings')
    parser.add_argument('-v', '--verbose', action='store_true',
            help='verbose logging output')
    parser.add_argument('-a', '--apps', action='store', nargs='+', type=int,
            help='include only these app IDs in the output')
    parser.add_argument('-c', '--countries', action='store', nargs='+',
            type=lambda x: str(x).upper(), choices=countries,
            help='list of ISO-3166-1 Alpha-2 country codes to query')
    parser.add_argument('-o', '--output', action='store',
            default='rankings.csv', type=argparse.FileType('wb'),
            help='CSV-formatted output file (default: %(default)s)')
    args = parser.parse_args(argv)

    if args.apps and args.verbose:
        print 'Apps: ' + ', '.join([str(app) for app in args.apps])

    if args.countries and args.verbose:
        print 'Countries: ' + ', '.join(args.countries)

    # Initialize our CSV output file.
    args.output.write(u'\ufeff'.encode('utf-8')) # BOM
    output = csv.DictWriter(args.output,
            ['country', 'device', 'category', 'list', 'rank', 'name',
             'appid', 'timestamp'])
    output.writeheader()

    for country_code, country in countries.iteritems():
        # Skip any unrequested countries.
        if args.countries and country_code not in args.countries:
            continue

        # Run all of our ranking queries for this country.
        for ranking, query in queries.iteritems():
            if args.verbose:
                print 'Fetching %s-%s-%s-%s' % (country_code, ranking[0],
                                                ranking[1], ranking[2])

            # Create a new row dictionary for this batch of items.
            row = {
                'country':      country.name,
                'device':       ranking[0],
                'category':     ranking[1],
                'list':         ranking[2],
                'timestamp':    str(datetime.datetime.utcnow()),
            }

            # For each item scraped from this query's results, update its
            # values in the current row and write it to the CSV file.
            for item in scrape(query, country.storefront):
                if args.apps is None or item['appid'] in args.apps:
                    row.update(item)
                    output.writerow(row)

if __name__ == '__main__':
    main(sys.argv[1:])
