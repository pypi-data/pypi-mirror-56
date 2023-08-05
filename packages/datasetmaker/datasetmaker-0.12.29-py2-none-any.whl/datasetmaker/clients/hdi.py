from pathlib import Path
from typing import Any, Union

import pandas as pd

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import _map, sid_to_id


class HDIClient(Client):
    """Client for Human Development Index."""

    url = ('http://ec2-54-174-131-205.compute-1.amazonaws.com/'
           'API/hdro_api_all.json')

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get data."""
        iso3_to_id = _map('country', 'iso3', 'country')
        df = (pd.read_json(self.url)
              .assign(country=lambda x: x.country_code.str.lower().map(iso3_to_id))
              .assign(indicator_name=lambda x: x.indicator_name.map(sid_to_id('hdi')))
              .drop(['country_code', 'country_name', 'indicator_id'], axis=1)
              .pivot_table(columns='indicator_name', index=['country', 'year'], values='value')
              .reset_index())

        self.data = df
        return df

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save data."""
        for indicator in self.data.columns.drop(['country', 'year']):
            self.data.ddf.register_datapoints(measures=indicator, keys=['country', 'year'])

        self.data.ddf.register_entity('country')

        package = DataPackage(self.data, dataset='hdi')
        package.save(path, **kwargs)
