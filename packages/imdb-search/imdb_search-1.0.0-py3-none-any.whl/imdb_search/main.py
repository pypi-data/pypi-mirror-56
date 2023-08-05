#!/usr/bin/env python3

import sys
import argparse
import requests
import json
from pick import pick
import datetime

# Using The Movie DB
# See https://www.themoviedb.org/documentation/api
BASE_URL = 'https://api.themoviedb.org/3'
# API key would normally be stored in environment variable or config, however has been made public for ease of setup
API_KEY = '3ede362e07be66c7640ff6ccf0d15994'


def GET(url, params={}):
    # Perform get requests using requests library
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Connection': 'close'}

    try:
        response = requests.request('GET', url, params=params, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'

        return response.json()
    except:
        print("Network error, movies could not be loaded. Please try again later.")
        sys.exit(1)


def search(name):
    # Search the movie database for name, return results
    url = f'{BASE_URL}/search/person?api_key={API_KEY}'
    params = {'query': name}
    data = GET(url, params)
    results = data['results']

    return results


def getMovies(person_id, reverse=False):
    # Fetch all movies for the given person
    url = f'{BASE_URL}/person/{person_id}/movie_credits?api_key={API_KEY}'

    data = GET(url)

    movies = (data)['cast']
    movies = sorted(movies, key=lambda x: datetime.datetime.strptime(
        x['release_date'], '%Y-%m-%d') if x['release_date'] else datetime.datetime.now(), reverse=reverse)

    return movies


def printMovies(person, movies):
    # Print movies to the console
    print('Showing movies for {}:'.format(person['name']))
    for movie in movies:
        print('\t{}\t{}'.format(
            movie['release_date'][:4], movie['original_title']))


def saveMovies(movies, filestream):
    # Save movies to a file, using a filestream
    filestream.write(json.dumps(movies, indent=4))
    filestream.close()


def main():
    # Setup command line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='name of the actor/actress to search for')
    parser.add_argument('-r', '--reverse',
                        help='return movies in reverse order (most recent first)', action='store_true')
    parser.add_argument(
        '-o', '--output', metavar='filename', help='save results to file in JSON format', type=argparse.FileType('w'))
    args = parser.parse_args()

    if not(args.name):
        print("Name cannot be blank")
        sys.exit(1)

    # Search the database for matches
    results = search(args.name)
    if len(results) == 0:
        print('No results for that name.')
        sys.exit(0)
    elif len(results) == 1:
        person = results[0]
    else:
        title = 'Please select an actor/actress:'
        options = list(map(lambda x: x['name'], results))
        _option, index = pick(options, title)
        person = results[index]

    # Fetch all movies for the person
    movies = getMovies(person['id'], reverse=args.reverse)
    printMovies(person, movies)

    # Save to file if output is specified
    if args.output:
        saveMovies(movies, args.output)


if __name__ == '__main__':
    main()
