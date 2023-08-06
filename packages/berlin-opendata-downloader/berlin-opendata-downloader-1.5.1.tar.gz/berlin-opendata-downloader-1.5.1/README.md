
# Download Client for Berlin Geländemodelle

[![PyPI version](https://badge.fury.io/py/berlin-opendata-downloader.svg)](https://badge.fury.io/py/berlin-opendata-downloader) [![PyPI downloads month](https://img.shields.io/pypi/dm/berlin-opendata-downloader.svg)](https://img.shields.io/pypi/dm/berlin-opendata-downloader.svg) [![PyPI downloads week](https://img.shields.io/pypi/dw/berlin-opendata-downloader.svg)](https://img.shields.io/pypi/dw/berlin-opendata-downloader.svg) [![PyPI downloads day](https://img.shields.io/pypi/dd/berlin-opendata-downloader.svg)](https://img.shields.io/pypi/dm/berlin-opendata-downloader.svg) 

Downloads [Berlins' height information](https://www.stadtentwicklung.berlin.de/geoinformation/landesvermessung/atkis/de/dgm.shtml) (Digitale Geländemodelle – ATKIS DGM - Höheninformationen), can compress them on the fly, and creates GeoJSON, CSV or txt files if desired.

**Documentation:** https://berlin-gelaendemodelle-downloader.readthedocs.io/en/latest/


## What means 'Compress'

Compression means tiles, shaped as windows, are averaged. Because one subset of the data is of shape `2000x2000`, the tile size, argument `compress`, have to divide 2000 without remainder.

The following image ([Original](http://fbarc.stadt-berlin.de/FIS_Broker_Atom//Blattschnitte/2X2_EPSG_25833.gif)) shows the structure of the data subsets (tiles).

![Data Tiles](http://fbarc.stadt-berlin.de/FIS_Broker_Atom//Blattschnitte/2X2_EPSG_25833.gif)


## Getting Started

Follow these instructions to get the `berlin-downloader` up and running.


### Prerequisites

- python 3.6 or greater
- pip3


### Installation

```bash
pip3 install berlin-opendata-downloader
```

or directly from the repository:

```bash
git clone https://github.com/se-jaeger/berlin-gelaendemodelle-downloader
cd berlin-gelaendemodelle-downloader
python setup.py install
```


### Example Usage

```bash
berlin_downloader download ~/berlin_height --compress 5 --keep_original --file-format csv --file-format geojson
```

Downloads and saves the data at `~/berlin_height` as vsc and geojson file, as well as compressed csv and geojson files.


## Thank You! :heart:

Many thanks to [chrisschroer](https://github.com/chrisschroer) for the offline discussions and contributions.


## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
