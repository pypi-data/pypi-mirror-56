import logging
import shutil
from pathlib import Path
from typing import Any, Union

import pandas as pd
import requests

from .meps import get_meps

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client

log = logging.getLogger(__name__)


class RiksdagenClient(Client):
    """Client for the Swedish Parliament."""

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        if kwargs['subset'] == 'meps':
            data = list(get_meps())
        else:
            raise ValueError('Not a valid subset')

        self.data = data
        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        log.info('Creating DataPackage')
        package = DataPackage(self.data, dataset='riksdagen')
        package.save(path, **kwargs)
        log.info('Datapackage successfully created')
        self._download_images(Path(path))

    def _download_images(self, path: Path) -> None:
        log.info('Downloading images')
        img_path = (path / 'images')
        img_path.mkdir()
        for _, row in self.data[0].iterrows():
            r = requests.get(row.image_url, stream=True)
            if r.status_code != 200:
                continue
            with open(img_path / f'mep_swe--{row.mep_swe}--portrait.jpg', 'wb') as f:
                shutil.copyfileobj(r.raw, f)
