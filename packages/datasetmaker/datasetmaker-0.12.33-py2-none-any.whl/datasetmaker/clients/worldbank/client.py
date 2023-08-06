import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Union

import pandas as pd

from .api import get_data_by_indicator, get_indicators_by_source
from .config import non_countries

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import _map, sid_to_id

log = logging.getLogger(__name__)


class WorldBank(Client):
    """Client for World Bank data."""

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        self.indicators: list = kwargs.get('indicators', [])
        subset = kwargs.get('subset')
        mrv = kwargs.get('n_latest_years', 2)

        data = []

        if self.indicators and subset:
            raise ValueError('Pass indicators or subset, not both')
        elif not self.indicators and not subset:
            raise ValueError('Must pass either indicators or subset')
        elif subset:
            self.indicators = get_indicators_by_source(subset)
        with ThreadPoolExecutor(max_workers=5) as executor:
            for frame in executor.map(get_data_by_indicator,
                                      self.indicators,
                                      [mrv] * len(self.indicators)):
                if frame is None or frame.empty:
                    continue
                frame = frame.dropna(subset=['value'])
                data.append(frame)
                data.append(frame)

        if not data:
            return

        df = pd.concat(data, sort=True).reset_index(drop=True)
        df = df.drop(['decimal', 'obs_status', 'unit', 'indicator.value'], axis=1)

        # Remove non-countries
        df['countryiso3code'] = df['countryiso3code'].fillna(df['country.id'])
        df = df.drop('country.id', axis=1)
        df = df[df['countryiso3code'] != '']
        df = df[~df['countryiso3code'].isin(non_countries)]

        # TODO: Make issue out of this special case
        df = df[df['country.value'] != 'West Bank and Gaza']

        # World Bank specific naming
        df['country.value'] = df['country.value'].replace('Taiwan, China', 'Taiwan')

        # Standardize country identifiers
        iso3_to_id = _map('country', 'iso3', 'country')
        name_to_id = _map('country', 'name', 'country')
        df['country'] = df['countryiso3code'].str.lower().map(iso3_to_id)
        df['country'] = df.country.fillna(df['country.value'].map(name_to_id))
        df = df.drop(['country.value', 'countryiso3code'], axis=1)
        df = df[df.country.notnull()]
        df = df.rename(columns={'indicator.id': 'indicator', 'date': 'year'})

        # Standardize indicator identifiers
        df.indicator = df.indicator.map(sid_to_id('worldbank'))

        df = df.pivot_table(index=['country', 'year'],
                            values='value', columns='indicator')
        df = df.reset_index()

        self.data = df
        return df

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        if not hasattr(self, 'data'):
            log.info('No data to package. Quitting.')
            return

        log.info('Creating datapackage')
        self.data.ddf.register_entity('country')
        for indicator in self.data.columns.drop(['country', 'year']):
            self.data.ddf.register_datapoints(measures=indicator, keys=['country', 'year'])
        package = DataPackage(self.data, dataset='worldbank')
        package.save(path, **kwargs)
        log.info('Datapackage successfully created')
