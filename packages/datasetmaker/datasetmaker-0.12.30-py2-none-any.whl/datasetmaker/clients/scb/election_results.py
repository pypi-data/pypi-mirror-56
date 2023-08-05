import logging

import pandas as pd

from datasetmaker.clients.scb.api import get_table_data
from datasetmaker.onto.manager import _map

log = logging.getLogger(__name__)


def get_election_results() -> pd.DataFrame:
    """
    Get election results from SCB.

    Returns
    -------
    pd.DataFrame
        Election dataframe.
    """
    data = _make_request()
    df = _format_response(data)

    df.ddf.register_datapoints(measures=['votes_tot', 'votes_share'],
                               keys=['party', 'year'])
    df.ddf.register_entity('party')

    return df


def _make_request() -> dict:
    log.info('Fetching historical election results')
    url = 'http://api.scb.se/OV0104/v1/doris/sv/ssd/START/ME/ME0104/ME0104C/ME0104T3'
    query = {
        'query': [
            {
                'code': 'Region',
                'selection': {
                    'filter': 'vs:RegionValkretsTot99',
                    'values': [
                        'VR00',
                    ],
                },
            },
        ],
        'response': {
            'format': 'json',
        },
    }

    return get_table_data(url, query)  # type: ignore


def _format_response(data: dict) -> pd.DataFrame:
    rows = [x['key'] + x['values'] for x in data['data']]
    df = pd.DataFrame(rows, columns=['region', 'party', 'year', 'votes_tot', 'votes_share'])
    df = df.replace('..', '0')
    df = df.drop('region', axis=1)
    df.party = df.party.str.lower()
    df = df[df.party.isin(['m', 'c', 'fp', 'kd', 'mp', 's', 'v', 'sd', 'övriga'])]
    df.party = df.party.str.replace('övriga', 'oth')
    df.party = df.party.str.replace('fp', 'l')
    df.party = df.party.map(_map('party', 'abbr', 'party', include_synonyms=False))
    df.votes_tot = df.votes_tot.astype(int)
    df.votes_share = df.votes_share.astype(float)
    df.year = df.year.astype(int)
    return df
