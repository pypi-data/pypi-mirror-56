import logging
import socket
import time
from typing import Optional

import pandas as pd
import requests
import urllib3

from .config import sources

log = logging.getLogger(__name__)


def make_request(url: str, params: dict = None) -> Optional[requests.models.Response]:
    """
    Make a request to the World Bank API.

    The API throws seemingly random errors from time to time.
    If such an error is encountered, sleep for 2 seconds and
    make one more attempt before failing.

    Parameters
    ----------
    url
        URL.
    params
        GET request parameters.

    Returns
    -------
    dict
        Dict with API data if request succeeded, else None.
    """
    try:
        resp = requests.get(url, params, timeout=20)
        if resp.status_code != 200:
            time.sleep(2)
            resp = requests.get(url, params, timeout=20)
    except socket.timeout:
        log.error(f'URL {url} timed out')
        return None
    except requests.exceptions.ReadTimeout:
        log.error(f'URL {url} timed out')
        return None
    except urllib3.exceptions.ReadTimeoutError:
        log.error(f'URL {url} timed out')
        return None
    except socket.gaierror:
        log.error(f'URL {url} raised gaiaerror')
        return None

    return resp


def get_all_pages(url: str, params: dict) -> list:
    """
    Get data for all pages for a given endpoint.

    Parameters
    ----------
    url
        URL.
    params
        GET request parameters.

    Returns
    -------
    list
        A list of all data objects.
    """
    params['page'] = 1
    last_page = -1
    data: list = []

    while last_page != params['page']:
        resp = make_request(url, params)
        if not resp:
            continue
        jdata = resp.json()

        if len(jdata) == 1 and 'message' in jdata and jdata['message'][0]['id'] == '175':
            log.warn(f'URL {url} was not found. It may have been deleted or archived')
            continue

        meta, page_data = jdata
        last_page = meta['pages']
        params['page'] = params['page'] + 1
        if page_data is None:
            continue
        data.extend(page_data)
        if last_page == 1:
            break

    return data


def get_indicators_by_source(source: str) -> list:
    """
    Fetch all available indicators from `source`.

    Parameters
    ----------
    source
        Source id or abbreviation.

    Returns
    -------
    list
        List of available indicators.
    """
    if source.isdigit():
        code = source
    else:
        code = sources[source.upper()]['id']
    url = f'https://api.worldbank.org/v2/source/{code}/indicator'
    params: dict = {'format': 'json'}
    data = get_all_pages(url, params)
    return [x['id'] for x in data]


def get_data_by_indicator(indicator: str, mrv: int) -> Optional[pd.DataFrame]:
    """
    Get data for a specific World Bank indicator.

    Parameters
    ----------
    indicator
        Indicator code.
    mrv
        Most recent values, i.e. n latest years.

    Returns
    -------
    pd.DataFrame
        Indicator data in dataframe if response succeeded, else None.
    """
    url = f'https://api.worldbank.org/v2/country/all/indicator/{indicator}'
    params = {'format': 'json', 'mrv': mrv, 'per_page': 200}
    data = get_all_pages(url, params)
    return api_data_to_frame(data) if data else None


def get_data_by_source(source: str, mrv: int) -> Optional[pd.DataFrame]:
    """
    Get data for a specific World Bank source.

    Parameters
    ----------
    source
        Source code.
    mrv
        Most recent values, i.e. n latest years.

    Returns
    -------
    pd.DataFrame
        Indicator data in dataframe if response succeeded, else None.
    """
    frames = []
    indicators = get_indicators_by_source(source)
    for indicator in indicators:
        indicator_data = get_data_by_indicator(indicator, mrv)
        frames.append(indicator_data)

    df = pd.concat(frames, sort=True)
    return df


def api_data_to_frame(data: list) -> pd.DataFrame:
    """
    Normalize the JSON API data and convert to dataframe.

    Parameters
    ----------
    data
        API response JSON data.

    Returns
    -------
    pd.DataFrame
        A normalized dataframe.
    """
    df = pd.DataFrame(data)

    # Expand all dict columns
    for col in df.columns.copy():
        try:
            expanded = pd.io.json.json_normalize(
                df[col], record_prefix=True)
            expanded.columns = [f'{col}.{x}' for x in expanded.columns]
            df = pd.concat([df, expanded], axis=1)
            df = df.drop(col, axis=1)
        except AttributeError:
            continue

    return df
