import logging
from pathlib import Path
from typing import Any, Union

import pandas as pd

from .election_results import get_election_results
from .psu_polls import get_psu_data

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client

log = logging.getLogger(__name__)


class SCBClient(Client):
    """
    Client for the Swedish statistical agency Statistiska Centralbyrån.

    Fetches data from a number of selected tables.
    """

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        psu_data = get_psu_data()
        election_results = get_election_results()

        self.data = [psu_data, election_results]
        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        log.info('Creating DataPackage')
        package = DataPackage(self.data, dataset='scb')
        package.save(path, **kwargs)
        log.info('Datapackage successfully created')
