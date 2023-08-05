"""
Fetching and parsing data from the school unit registry.

http://api.scb.se/UF0109/v2/Help
"""

import datetime
import logging
from concurrent.futures import ThreadPoolExecutor

import requests

from datasetmaker.utils import RateLimiter

log = logging.getLogger(__name__)

api_rate_limiter = RateLimiter(0.05)


def fetch_school_unit_data(code: str) -> dict:
    """
    Fetch school data from external API.

    Parameters
    ----------
    code
        School unit code.
    """
    look_back_years = 5
    date_format = '%Y%m%d'
    start_date = datetime.datetime.now().date()
    date = start_date
    base_url = 'http://api.scb.se/UF0109/v2/skolenhetsregister/sv/skolenhet/{}/{}'
    finished = False
    data: dict = {}

    while finished is False:
        url = base_url.format(code, date.strftime(date_format))
        r = requests.get(url)
        if r.status_code != 200:
            if start_date.year - date.year > look_back_years:
                finished = True
            else:
                date = date - datetime.timedelta(days=365)
                continue
        finished = True
        data = r.json()

    if 'Message' in data:  # Error message
        log.error(f'{code}: {data["Message"]}')
        data = {}

    return data


def parse_school_unit_data(data: dict) -> dict:
    """
    Parse a school data API response object.

    Parameters
    ----------
    data
        School unit data object.
    """
    if not data:  # empty dict
        return data
    data = data['SkolenhetInfo']
    primary_school_years = []
    primary_school_year_labels = [f'Ak{x}' for x in range(1, 10)]
    primary_school_data = [x for x in data['Skolformer'] if x['Benamning'] == 'Grundskola']
    if primary_school_data:
        for label in primary_school_year_labels:
            if primary_school_data[0][label]:
                primary_school_years.append(label[-1])

    parsed = {
        'school_unit': data['Skolenhetskod'],
        'name': data['Namn'],
        'school_name': data['SkolaNamn'],
        'huvudman': data['Huvudman']['Namn'],
        'huvudman_type': data['Huvudman']['Typ'],
        'municipality': data['Kommun']['Kommunkod'],
        'is_high_school': 'Gymnasieskola' in (x['Benamning'] for x in data['Skolformer']),
        'is_primary_school': 'Grundskola' in (x['Benamning'] for x in data['Skolformer']),
        'primary_school_years': ','.join(primary_school_years),
        'lat': data['Besoksadress']['GeoData']['Koordinat_WGS84_Lat'],
        'lng': data['Besoksadress']['GeoData']['Koordinat_WGS84_Lng'],
        'url': data['Webbadress'],
    }

    try:
        parsed['lat'] = float('%.3f' % float(parsed['lat']))
        parsed['lng'] = float('%.3f' % float(parsed['lng']))

    # Not possible to cast coordinates to floats,
    # usually because they're empty strings
    except ValueError:
        parsed['lat'] = None
        parsed['lng'] = None

    # Coordinates are None
    except TypeError:
        pass

    parsed['fetched_at'] = datetime.datetime.now().date().strftime('%Y-%m-%d')

    return parsed


def fetch_and_parse_school_unit_data(code: str) -> dict:
    """
    Fetch school data from external API and parse it, at once.

    Parameters
    ----------
    code
        School unit code.
    """
    next(api_rate_limiter)
    data = fetch_school_unit_data(code)
    try:
        parsed = parse_school_unit_data(data)
    except ValueError:
        logging.error(f'ValueError: {code}')
        parsed = {}
        pass
    except KeyError:
        logging.error(f'KeyError: {code}')
        parsed = {}
        pass
    return parsed


def get_school_registry_data(codes: list, max_workers: int = 50) -> list:
    """
    Get school unit data for a list of school units.

    Parameters
    ----------
    codes
        School unit codes.
    max_workers
        Maximum number of threads.
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for data in executor.map(fetch_and_parse_school_unit_data, codes):
            results.append(data)

    return results
