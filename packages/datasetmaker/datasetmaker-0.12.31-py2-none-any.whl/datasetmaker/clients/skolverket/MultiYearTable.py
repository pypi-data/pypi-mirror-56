from pathlib import Path
from typing import Union

import pandas as pd

from .Table import Table


class MultiYearTable:
    """
    Representation of multiple years of data for a given table.

    Parameters
    ----------
    code
        Table code.
    uttag
        Skolverket uttag parameter.
    year_codes
        List of years to include.
    cache_dir
        Directory to write cached files to.
    """

    _entities: list = []

    def __init__(self, code: str, uttag: str, year_codes: list, cache_dir: Union[str, Path]):
        self.code = code
        self.uttag = uttag
        self.year_codes = year_codes
        self.cache_dir = cache_dir

    @property
    def entities(self) -> list:
        """Get all entities."""
        if len(self._entities) > 0:
            return self._entities
        self._entities = Table(self.code, self.uttag, self.year_codes[0], self.cache_dir).entities
        return self._entities

    @property
    def data(self) -> pd.DataFrame:
        """Get the data."""
        tables = [Table(self.code, self.uttag, y, self.cache_dir) for y in self.year_codes]
        tables = [t.data for t in tables if not t.data.empty]
        if not tables:
            return pd.DataFrame()
        return pd.concat(tables, sort=True)

    def __repr__(self) -> str:
        return f'<MultiYearTable code="{self.code}" years={str(self.year_codes)}>'

    def __str__(self) -> str:
        return f'<MultiYearTable code="{self.code}" years={str(self.year_codes)}>'
