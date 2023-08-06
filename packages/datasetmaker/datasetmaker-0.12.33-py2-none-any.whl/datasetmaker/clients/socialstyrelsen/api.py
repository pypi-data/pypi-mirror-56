import logging
import socket
import time
from typing import Optional

import requests
import urllib3

log = logging.getLogger(__name__)


def make_request(url: str) -> Optional[requests.models.Response]:
    """
    Make a request to the Socialstyrelsen API.

    If an error is encountered, sleep for 2 seconds and
    make one more attempt before failing.

    Parameters
    ----------
    url
        URL.

    Returns
    -------
    requests.models.Response
        Response object if request succeeded, else None.
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
