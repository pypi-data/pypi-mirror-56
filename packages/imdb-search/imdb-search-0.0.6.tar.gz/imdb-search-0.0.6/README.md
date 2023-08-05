# IMDB Search

A small CLI to search for movies than an actor/actress has starred in.

## Installation
```
pip3 install imdb-search
```

## Usage
```
usage: imdb-search [-h] [-r] [-o filename] name

positional arguments:
  name                  name of the actor/actress to search for

optional arguments:
  -h, --help            show this help message and exit
  -r, --reverse         return movies in reverse order (most recent first)
  -o filename, --output filename
                        save results to file in JSON format
```