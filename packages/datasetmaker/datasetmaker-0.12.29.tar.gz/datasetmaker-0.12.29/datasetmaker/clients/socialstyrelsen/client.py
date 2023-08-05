from pathlib import Path
from typing import Any, Union

import pandas as pd

from .deaths import get_deaths

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client


class SocialstyrelsenClient(Client):
    """Client for the Swedish agency Socialstyrelsen."""

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        subset = kwargs.get('subset', '')
        if subset == 'deaths':
            self.data = get_deaths()
        else:
            raise NotImplementedError('Only deaths subset available.')

        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save data."""
        package = DataPackage(self.data)
        package.save(path, **kwargs)
