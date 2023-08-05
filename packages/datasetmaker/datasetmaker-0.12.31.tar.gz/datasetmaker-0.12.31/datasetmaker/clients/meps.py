from pathlib import Path
from typing import Any, Union

import defusedxml.ElementTree as ET
import pandas as pd
import requests

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import _map, sid_to_id
from datasetmaker.utils import etree_to_dict, nice_string


class MEPs(Client):
    """Read members of parliament from the oficial API."""

    url = 'https://www.europarl.europa.eu/meps/en/full-list/xml/'

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        r = requests.get(self.url)
        xml_data = ET.fromstring(r.content)
        data = etree_to_dict(xml_data)['meps']['mep']
        df = self.transform(pd.DataFrame(data))
        df['country'] = df.country.map(_map('country', 'name', 'country'))
        df['first_name'] = df.fullName.str.split(expand=True)[0]
        df['last_name'] = df.fullName.str.split().apply(
            lambda x: ' '.join(x[1:]))
        df['last_name'] = df.last_name.map(lambda x: nice_string(x,
                                                                 case='title',
                                                                 replace_accents=False,
                                                                 replace_special=None))

        df['meps_mep'] = df.fullName.str.replace(' ', '_')
        df['meps_mep'] = df.meps_mep.map(lambda x: nice_string(x,
                                                               case='lower',
                                                               replace_accents=True,
                                                               replace_special=''))

        df = df.drop('fullName', axis=1)

        df.columns = df.columns.map(sid_to_id('meps'))

        self.data = df
        return self.data

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform the data."""
        data = data.drop('id', axis=1)
        return data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        self.data.ddf.register_entity('country')
        self.data.ddf.register_entity('meps_mep')
        self.data.ddf.register_entity('meps_national_political_group')
        self.data.ddf.register_entity('meps_political_group')

        package = DataPackage(self.data, dataset='meps')
        package.save(path, **kwargs)
