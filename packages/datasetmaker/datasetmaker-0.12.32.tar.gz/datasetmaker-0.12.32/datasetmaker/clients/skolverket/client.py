import datetime
import logging
import os
import shutil
from functools import reduce
from pathlib import Path
from typing import Any, Union

import numpy as np
import pandas as pd
import requests

from .concepts import concepts
from .MultiYearTable import MultiYearTable
from .school_registry import get_school_registry_data

from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import read_entity
from datasetmaker.path import ROOT_DIR
from datasetmaker.utils import flatten, pluck

log = logging.getLogger(__name__)


_base_url = 'https://siris.skolverket.se/siris/reports'
_cache_dir = os.path.join(ROOT_DIR, '.cache_dir')
_form_codes = ['11', '21']  # Grundskolan, Gymnasieskolan


class SkolverketClient(Client):
    """Client for Swedish school data from Skolverket."""

    _schema: list = []

    @property
    def indicators(self) -> list:
        """Get all indicators for the dataset."""
        out = []
        exc = [70, 71, 93, 12, 49, 21, 193, 199, 196, 200, 102, 2, 1, 4,
               123, 83, 202, 201, 54, 65, 64, 106, 263, 55, 206, 205]
        for concept in concepts:
            if concept['concept_type'] == 'measure' and int(concept['table']) not in exc:
                out.append(concept['concept'])
        return out

    def _validate_input(self, indicators: list, years: list) -> None:
        concept_names = pluck(concepts, 'concept')
        for indicator in indicators:
            if indicator not in concept_names:
                raise ValueError(f'{indicator} is not a valid indicator')
            available_years = pluck(self.schema, 'år')
            available_years = [x['kod'] for x in flatten(available_years)]
            for year in years:
                if year not in available_years:
                    raise ValueError(f'{year} is not available in any table')

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        indicators: Any = kwargs.get('indicators', self.indicators)
        years: Any = kwargs.get('years')
        cache_dir: Any = kwargs.get('cache_dir')
        if not cache_dir:
            self.cache_dir = Path(_cache_dir)
        else:
            self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        years = [str(x) for x in years]

        # Validate indicators and years
        log.info('Validating indicators and years')
        self._validate_input(indicators, years)

        # Fetch data remotely
        frames = []
        entities = set()
        schemas = self._table_schemas_from_concepts(indicators)
        for schema in schemas:
            _years = [x for x in years if str(x) in pluck(schema['år'], 'kod')]
            log.debug(f'Creating MultiYearTable {schema["kod"]}')
            table = MultiYearTable(schema['kod'], schema['uttag'], _years, self.cache_dir)
            if table.data.empty:
                continue
            frames.append(table.data)
            entities.update(table.entities)
        if not frames:
            return
        keys = list(entities)
        for frame in frames:
            for key in keys:
                if key not in frame:
                    frame[key] = None

        log.info('Merging MultiYearTables')
        df = reduce(lambda l, r: pd.merge(l, r, on=keys, how='outer'), frames)

        for indicator in indicators:
            if indicator not in df:
                log.warn(f'{indicator} not in df')

        df = df.filter(items=indicators + keys)

        # Clean data
        log.info('Cleaning data')
        df = df.pipe(self._clean_data)

        log.info('Configuring DDF')
        self.data = df.set_index(keys)
        self.data = self._config_ddf(self.data)

        school_units = self._update_school_units_from_registry()
        self.data.ddf.override_entity('school_unit', school_units)

        return self.data

    def _update_school_units_from_registry(self) -> pd.DataFrame:
        """Get school unit entities from ontology and update any missing rows."""
        units = read_entity('school_unit')
        units.fetched_at = pd.to_datetime(units.fetched_at)
        expired = units[(datetime.datetime.now() - units.fetched_at).dt.days > 90]
        expired_codes = expired.school_unit.to_list()
        missing = self.data[~self.data.school_unit.isin(units.school_unit)]
        missing_codes = missing.school_unit.to_list()
        if not (expired_codes + missing_codes):
            return units
        units = units[~units.school_unit.isin(expired_codes + missing_codes)]
        fresh = get_school_registry_data(expired_codes + missing_codes)
        fresh = pd.DataFrame(fresh)
        return pd.concat([units, fresh], sort=True).reset_index(drop=True)

    def _config_ddf(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Register datapoints and entities to data.

        Parameters
        ----------
        data
            Input dataframe.
        """
        datapoints = []
        entities = []
        for col in data.columns:
            sub = data[col].dropna().reset_index().dropna(axis=1)
            if not sub.empty:
                entities.extend(list(sub.columns.drop(col)))
                datapoints.append((col, list(sub.columns.drop(col))))
        entities = list(set(entities))
        try:
            entities.remove('year')
        except ValueError:
            pass

        data = data.reset_index()
        for entity in entities:
            data.ddf.register_entity(entity)
        for datapoint in datapoints:
            data.ddf.register_datapoints(datapoint[0], datapoint[1])

        return data

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace(['..', '.'], [None, None])
        df = df.replace(',', '.', regex=True)
        df = df.replace('~100', '100')
        df = df.replace({r'(\d) (\d)': r'\1\2'}, regex=True)

        for col in df.columns:
            if col in (x['concept'] for x in concepts if x['concept_type'] == 'measure'):
                df[col] = df[col].astype(np.float64)

        return df

    def clear_cache(self) -> None:
        """Clear the cache from disk."""
        shutil.rmtree(self.cache_dir)

    @property
    def schema(self) -> list:
        """Get dataset schema."""
        if self._schema:
            return self._schema
        _schema = []

        for form_code in _form_codes:
            areas_url = (f'{_base_url}/export_api/omrade/'
                         f'?pVerkform={form_code}&pNiva=S')
            areas = requests.get(areas_url).json()

            for area in areas:
                tables_url = (f'{_base_url}/export_api/export/?pVerkform='
                              f'{form_code}&pNiva=S&pOmrade={area["kod"]}')
                tables = requests.get(tables_url).json()

                for table in tables:
                    table['år'] = []
                    years_url = (f'{_base_url}/export_api/lasar/?pExportID='
                                 f'{table["kod"]}')
                    years = requests.get(years_url).json().get('data')

                    for year in years:
                        table['år'].append(year)

                    uttag_url = (f'{_base_url}/export_api/extra/?pExportID='
                                 f'{table["kod"]}&pAr={years[0]["kod"]}')
                    uttag = requests.get(uttag_url).json()
                    if len(uttag['uttag']) == 0:
                        table['uttag'] = 'null'
                    else:
                        table['uttag'] = uttag['uttag'][0]['kod']

                    table.pop('egenskaper')
                    _schema.append(table)
        self._schema = _schema
        return _schema

    def _table_schemas_from_concepts(self, concept_names: list) -> list:
        schemas: list = []
        codes: list = []
        for concept in concept_names:
            table_code = [x['table'] for x in concepts if  # type: ignore
                          x['concept'] == concept][0]  # type: ignore
            schema = [x for x in self.schema if x['kod'] == table_code][0].copy()
            if schema['kod'] not in codes:
                schemas.append(schema)
                codes.append(schema['kod'])
        return schemas

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        if self.data.empty:
            raise ValueError('Client has no data')
        package = DataPackage(self.data, dataset='skolverket')
        package.save(path, **kwargs)
