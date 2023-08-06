import logging
import socket
import time
from typing import Optional

import pandas as pd
import requests
import urllib3

log = logging.getLogger(__name__)


def make_request(url: str) -> Optional[requests.models.Response]:
    """
    Make a request to the Kolada API.

    If an error is encountered, sleep for 2 seconds and
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
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            time.sleep(2)
            resp = requests.get(url, timeout=20)
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


def get_data_by_indicator(indicator: str, years: list) -> Optional[pd.DataFrame]:
    """
    Get data for a specific indicator.

    Parameters
    ----------
    indicator
        Indicator id.
    years
        List of years.
    """
    series: list = []

    for year in years:
        url = f'http://api.kolada.se/v2/data/kpi/{indicator}/year/{year}'
        r = make_request(url)

        if r and r.status_code == 200:
            series.extend(r.json().get('values'))
        else:
            continue

    if not series:
        log.error(f'No data for {indicator}')
        return None

    df = pd.io.json.json_normalize(series,
                                   record_path='values',
                                   meta=['kpi', 'municipality', 'period'])
    df.kpi = df.kpi.str.lower()
    return df
