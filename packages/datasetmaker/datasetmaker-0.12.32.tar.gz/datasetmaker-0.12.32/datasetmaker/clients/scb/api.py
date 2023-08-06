import json
from typing import Union

import requests


def get_table_data(url: str,
                   query: dict,
                   data_format: str = 'json') -> Union[dict, str]:
    """
    Get data from an SCB table.

    Use the query parameter to filter the data.

    Parameters
    ----------
    url
        Full URL to resource.
    query
        An SCB compliant query object.
    data_format : {'json', 'csv'}
        The response data format.

    Returns
    -------
    dict
        The response data.
    """
    r = requests.post(url, data=json.dumps(query))
    if r.status_code != 200:
        raise ValueError('SCB URL or query malformed. Status code: {r.status_code}')
    if data_format == 'csv':
        data = r.text
    else:
        data = json.loads(r.content.decode('utf-8-sig'))
    return data
