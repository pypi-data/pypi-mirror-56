import logging
from pathlib import Path
from typing import Any, Union

import pandas as pd

from .api import get_data_by_indicator, make_request

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import read_entity

log = logging.getLogger(__name__)


class KoladaClient(Client):
    """
    Client for Swedish municipality statistics from Kolada.

    Current limitations:
        - Does not include data by gender.
        - Discards data on non-municipalities, like municipality groups.
    """

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        indicators = kwargs.get('indicators', [])
        subset = kwargs.get('subset', '')
        years = kwargs.get('years', [2019])

        if not indicators and not subset:
            raise ValueError('Must pass indicators or subset.')
        elif indicators and subset:
            raise ValueError('Cannot pass both indicators and subset')
        elif subset:
            # If subset is an ID
            if subset.lower().startswith('g') and len(subset) <= 11 and subset.count(' ') == 0:
                url = f'http://api.kolada.se/v2/kpi_groups/{subset.upper()}'
            # If subset is a title
            else:
                url = f'http://api.kolada.se/v2/kpi_groups?title={subset}'
            r = make_request(url)
            if not r or r.status_code != 200:
                raise ValueError('No data found for subset {subset}')
            indicators = [x['member_id'] for x in r.json()['values'][0]['members']]  # type: ignore

        indicators = [x.lower() for x in indicators]

        frames = []
        for indicator in indicators:
            frame = get_data_by_indicator(indicator.upper(), years)
            frames.append(frame)

        municipalities = read_entity('municipality')  # noqa

        df = (pd.concat(frames, sort=True)
              .query('gender == "T"')
              .query('municipality.isin(@municipalities.municipality)')
              .drop(['count', 'status', 'gender'], axis=1)
              .rename(columns={'period': 'year'})
              .dropna(subset=['value'])
              .pivot_table(index=['municipality', 'year'],
                           columns='kpi',
                           values='value')
              .reset_index())

        if df.empty:
            raise ValueError('No data found. Perhaps the data is '
                             'only available for non-municipalities')

        df.ddf.register_entity('municipality')
        for indicator in indicators:
            if indicator not in df:
                continue
            df.ddf.register_datapoints(measures=indicator, keys=['municipality', 'year'])

        self.data = df
        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        package = DataPackage(self.data, dataset='kolada')
        package.save(path, **kwargs)
