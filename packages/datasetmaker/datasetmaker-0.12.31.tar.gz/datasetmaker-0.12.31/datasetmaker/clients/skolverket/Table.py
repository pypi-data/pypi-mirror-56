import io
import logging
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

import pandas as pd
import requests

from .concepts import concepts

from datasetmaker.utils import CSV_DTYPES

log = logging.getLogger(__name__)
_base_url = 'https://siris.skolverket.se/siris/reports'


class Table:
    """
    Representation of a single year of data for a given table.

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

    def __init__(self, code: str, uttag: str, year_code: list, cache_dir: Union[str, Path]):
        self.code = code
        self.uttag = uttag
        self.year_code = year_code
        self.cache_dir = cache_dir

        if self.cached:
            self.data = self._read_cache()
        else:
            xml = self._fetch_xml()
            frame = self._xml_to_frame(xml)
            if not frame.empty:
                self.data = frame
                self._write_table()
                self.data = self._read_cache()
            else:
                self.data = pd.DataFrame()

    @property
    def fname(self) -> str:
        """Get the table's file name."""
        return f'{self.code}-{self.year_code}.csv'

    @property
    def cached(self) -> bool:
        """Check whether the table is cached on disk."""
        return (Path(self.cache_dir) / self.fname).exists()

    @property
    def concepts(self) -> list:
        """List all concepts in the table."""
        if self.data.empty:
            return []
        items = []
        cols = self.data.columns
        for col in cols:
            item = next(filter(lambda x: x['concept'] == col, concepts))  # type: ignore
            items.append(item)
        return items

    @property
    def entities(self) -> list:
        """List all entities in the table."""
        concepts = self.concepts
        types = ['time', 'entity_domain']
        return [x['concept'] for x in concepts if x['concept_type'] in types]

    def _fetch_xml(self) -> str:
        log.info(f'Downloading {self}')
        url = (f'{_base_url}/export_api/runexport/?pFormat=xml'
               f'&pExportID={self.code}&pAr={self.year_code}'
               f'&pUttag={self.uttag}&pFlikar=1')
        r = requests.get(url)
        return r.text

    def _read_cache(self) -> pd.DataFrame:
        log.debug(f'Reading {self.fname} from disk')
        table = pd.read_csv(os.path.join(self.cache_dir, self.fname), dtype=CSV_DTYPES)
        # TODO: We drop metadata on schools here, do we need that info?
        table = table.drop(
            [x for x in table.columns if 'huvudman' in x or 'kommun' in x or 'skolnamn' in x],
            axis=1)
        table = table.rename(columns={'skolverket_kon': 'gender'})
        if 'gender' in table:
            table['gender'] = table['gender'].str.replace('Samtliga', 'all').str.replace(
                'Flickor', 'female').str.replace('Pojkar', 'male')
        return table

    def _write_table(self) -> None:
        log.info('Writing table to disk')
        self.data.to_csv(os.path.join(self.cache_dir, self.fname), index=False)

    def _xml_to_frame(self, xml: str) -> pd.DataFrame:
        data = []
        tree = ET.parse(io.StringIO(xml))
        root = tree.getroot()
        for s in root.findall('skola'):
            school = s.attrib
            for prop in s:
                school[prop.tag] = prop.text  # type: ignore
            data.append(school)
        df = pd.DataFrame(data)

        if df.empty:
            return df

        df['year'] = self.year_code
        sid_to_id = pd.DataFrame(concepts)
        alt = sid_to_id[sid_to_id.alt_spelling.notnull()].copy()
        alt.sid = alt.alt_spelling
        alt = alt.drop(['alt_spelling'], axis=1)
        sid_to_id = pd.concat([sid_to_id, alt], sort=True, axis=0)
        sid_to_id = sid_to_id[(sid_to_id.table == self.code) | (sid_to_id.table.isnull())]
        sid_to_id = sid_to_id.set_index('sid').concept.to_dict()
        df.columns = df.columns.map(sid_to_id)
        return df

    def __repr__(self) -> str:
        return f'<Table code="{self.code}" year={self.year_code}>'

    def __str__(self) -> str:
        return f'<Table code="{self.code}" year={self.year_code}>'
