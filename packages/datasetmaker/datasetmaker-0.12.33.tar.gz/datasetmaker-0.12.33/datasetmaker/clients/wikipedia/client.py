import logging
from pathlib import Path
from typing import Any, Union

from . import election_scraper, leader_scraper, visa_scraper

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client

log = logging.getLogger(__name__)

scrapers = [election_scraper, leader_scraper, visa_scraper]


class WikipediaClient(Client):
    """Client for Wikipedia data."""

    def get(self, **kwargs: Any) -> list:
        """Get the data by running each scrapers `scrape` function."""
        log.info('Scraping pages')
        self.data: list = []
        for scraper in scrapers:
            self.data.append(scraper.scrape())  # type: ignore
        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        log.info('Creating datapackage')
        package = DataPackage(self.data, dataset='wikipedia')
        package.save(path, **kwargs)

        log.info('Datapackage successfully created')
