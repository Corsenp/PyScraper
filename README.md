# PyScrapper

PyScrapper is a school project using selenium to get data out of a [website](https://wits.worldbank.org/CountryProfile/en/Country/FRA/Year/2017/TradeFlow/Export/Partner/by-country/Product/Total)

## Installation

Python 3 is required in order to run this program

### OSX

```bash
brew install python3
```

Then we install selenium with the package manager [pip](https://pip.pypa.io/en/stable/)
```bash
pip install selenium
```

If you have any trouble installing selenium go check the [official documentation](https://selenium-python.readthedocs.io/installation.html)

## Usage

```bash
$ scraper.py
Usage: scraper.py [COMMAND]

Command:
ISOCODE - Will print the Top 4 countries that received imports and the import amount in 2017 from the country ISOCODE
all     - Pick 4 random countries and print their respective Top 4 countries that received imports and the import amount in 2017
save    - Will save the result to a csv file named results.csv
```

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)