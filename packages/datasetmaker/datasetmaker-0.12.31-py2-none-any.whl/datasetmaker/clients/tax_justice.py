import io
from pathlib import Path
from typing import Any, Union

import pandas as pd

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import read_concepts
from datasetmaker.utils import read_private_github_file


class TaxJusticeClient(Client):
    """
    Client for the Tax Justice Network.

    This client fetches a pre-configured package from Github.
    """

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get data from private Github repository."""
        frames = []
        concepts = read_concepts()
        concepts = concepts[concepts.source == 'tax_justice']
        for concept in concepts.concept:
            url = ('https://raw.githubusercontent.com/datastory-org/raw-data/'
                   f'master/tax_justice/ddf--datapoints--{concept}--by--jurisdiction--year.csv')
            text = read_private_github_file(url).text
            frame = pd.read_csv(io.StringIO(text))
            frame.ddf.register_entity('jurisdiction')
            frame.ddf.register_datapoints(measures=concept, keys=['jurisdiction', 'year'])
            frames.append(frame)

        self.data = frames
        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        package = DataPackage(self.data, dataset='tax_justice')
        package.save(path, **kwargs)
