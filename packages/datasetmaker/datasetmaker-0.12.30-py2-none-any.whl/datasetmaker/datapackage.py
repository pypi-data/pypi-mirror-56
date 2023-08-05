import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
from ddf_utils import package
from ddf_utils.io import dump_json

from datasetmaker.onto.manager import entity_exists, read_concepts, read_entity
from datasetmaker.utils import CSV_DTYPES
from datasetmaker.validate import validate_package

log = logging.getLogger(__name__)


class DataPackage:
    """
    Class for automatically creating data packages from data frames.

    The input data should be prepped with `.ddf`-accessor properties
    so DataPackage knows how to treat entities, datapoints etc.

    The dataset parameter is used to read metadata for the package.

    Parameters
    ----------
    data
        Single or multiple input dataframes.
    dataset
        Dataset identifier.
    """

    def __init__(self,
                 data: Union[pd.DataFrame, List[pd.DataFrame]],
                 dataset: Optional[str] = None) -> None:
        self.data = data
        self.dataset = dataset

        if isinstance(data, pd.DataFrame):
            self._init_with_frame(data)
        elif isinstance(data, list) and all(isinstance(x, pd.DataFrame) for x in data):
            self._init_with_list_of_frames(data)
        else:
            raise TypeError(f'Data must be of type {pd.DataFrame} '
                            f'or list of {pd.DataFrame}, not {type(data)}.')

    def _init_with_frame(self, data: pd.DataFrame) -> None:
        """
        Initialize the class with a single dataframe.

        Parameters
        ----------
        data
            A single dataframe.
        """
        concepts = self._create_concepts(data)
        concepts = self._hydrate_concepts(concepts)
        self.concepts = concepts

        self.entities = self._create_entities(data)
        self.datapoints = self._create_datapoints(data)

        self._add_missing_concepts()
        self.concepts = self.concepts.drop_duplicates(subset=['concept'])

    def _init_with_list_of_frames(self, data: List[pd.DataFrame]) -> None:
        """
        Initialize the class with a list of dataframes.

        Parameters
        ----------
        data
            A list of dataframes.
        """
        concepts_frames = []
        for frame in data:
            concepts_frames.append(self._create_concepts(frame))
        concepts = pd.concat(concepts_frames, sort=True)
        concepts = concepts.drop_duplicates(subset=['concept'])
        concepts = self._hydrate_concepts(concepts)
        self.concepts = concepts

        self.entities = {}
        self.datapoints = {}
        for frame in data:
            eframes = self._create_entities(frame)
            pframes = self._create_datapoints(frame)

            for ename, eframe in eframes.items():
                if ename in self.entities:
                    self.entities[ename] = pd.concat([self.entities[ename], eframe], sort=True)
                    self.entities[ename] = self.entities[ename].drop_duplicates(subset=ename)
                else:
                    self.entities[ename] = eframe

            for pname, pframe in pframes.items():
                if pname in self.datapoints:
                    keys = pname.split('--by--')[-1].split('.')[0].split('--')
                    self.datapoints[pname] = pd.concat([self.datapoints[pname], pframe], sort=True)
                    self.datapoints[pname] = self.datapoints[pname].drop_duplicates(subset=keys)
                else:
                    self.datapoints[pname] = pframe

        self._add_missing_concepts()
        self.concepts = self.concepts.drop_duplicates(subset=['concept'])

    def _create_entities(self, frame: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Create a list of dicts mapping from entity names to entity frames.

        If the entity exists in the data ontology, merge it. Else just use `data`.

        Parameters
        ----------
        frame
            Input dataframe.

        Returns
        -------
        list
            List of dicts mapping entity name -> entity frame.
        """
        items: dict = {}
        for entity in frame.ddf.entities:
            entity_frame = frame.ddf.create_entity_frame(entity)
            entity_frame = self._hydrate_entity(entity_frame, entity)
            items[entity] = entity_frame
        return items

    def _create_datapoints(self, frame: pd.DataFrame) -> dict:
        items: dict = {}
        for measures, keys in frame.ddf.datapoints:
            pframe = frame[measures + keys]
            pframe = pframe.dropna(subset=measures + keys)
            items[f'ddf--datapoints--{"--".join(measures)}--by--{"--".join(keys)}.csv'] = pframe
        return items

    def _add_missing_concepts(self) -> None:
        """Recursively add missing concepts, e.g. entities referred to in other entities."""
        finished = False
        while not finished:
            missing: list = []
            concepts = self.concepts.copy()
            for entity_name, entity_frame in self.entities.items():
                cols = self._create_concepts(entity_frame)
                missing_frame = cols[~cols.concept.isin(concepts.concept)]
                missing.extend(missing_frame.concept.to_list())
            for col in concepts.columns:
                if col in ['concept', 'concept_type']:
                    continue
                if not (concepts.concept == col).any():
                    missing.append(col)
            if not missing:
                finished = True
            else:
                for miss in missing:
                    self.concepts = self.concepts.append({'concept': miss}, ignore_index=True)
                    self.concepts = self._hydrate_concepts(self.concepts)
                    row = self.concepts[self.concepts.concept == miss].iloc[0]
                    if row.concept_type == 'entity_domain':
                        self.entities[miss] = read_entity(miss)

    def _create_concepts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a DDF concepts dataframe from a given dataframe.

        The resulting dataframe will have only a `concept` column.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        Returns
        -------
        pd.DataFrame
            A simplied DDF concepts dataframe.
        """
        # Split columns by period to handle composite concepts
        cols = pd.Series(df.columns).str.split('.', expand=True)
        cols = pd.concat([cols[i] for i in range(cols.shape[1])])
        cols = pd.Series(cols).str.split('__', expand=True)
        cols = pd.concat([cols[i] for i in range(cols.shape[1])])
        cols = cols.dropna().drop_duplicates()

        return cols.to_frame(name='concept')

    def _hydrate_concepts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge `df` with ontology concepts, adding extra columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.

        Returns
        -------
        pd.DataFrame
            Merged dataframe.
        """
        return df[['concept']].merge(read_concepts(*df.concept.to_list(), recursive=False),
                                     on='concept',
                                     how='left')

    def _hydrate_entity(self, df: pd.DataFrame, name: str) -> pd.DataFrame:
        """
        Merge `df` with corresponding entity frame in the ontology, adding extra columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.
        name : str
            Name of entity.

        Returns
        -------
        pd.DataFrame
            Merged dataframe.
        """
        if not entity_exists(name):
            return df
        return df[[name]].merge(read_entity(name), on=name, how='left')

    def save(self, path: Union[Path, str], append: bool = False, **kwargs: str) -> None:
        """
        Save the data as a DDF data package.

        Parameters
        ----------
        path
            Directory path.
        append
            If package in `path` already exists, whether to append to it.
            If set to False, will remove the directory and re-create it.
        **kwargs
            Any additional keyword arguments are treated as package metadata.
        """
        files: dict = {}

        path = Path(path)
        if path.exists() and not append:
            shutil.rmtree(path)
        path.mkdir(exist_ok=True)

        # Prepare ddf--concepts
        files['ddf--concepts.csv'] = self.concepts

        # Prepare entity domain files
        for entity_name, entity_frame in self.entities.items():
            files[f'ddf--entities--{entity_name}.csv'] = entity_frame

        # Prepare datapoints files
        for data_name, data_frame in self.datapoints.items():
            files[data_name] = data_frame

        # Write all files to disk
        for fname, frame in files.items():
            if not (path / fname).exists():
                frame.to_csv(path / fname, index=False)
                continue
            old_frame = pd.read_csv(path / fname, dtype=CSV_DTYPES)
            frame = pd.concat([frame, old_frame], sort=True)
            frame = frame.drop_duplicates()
            frame.to_csv(path / fname, index=False)

        # Populate the package metadata object
        if self.dataset:
            meta = read_entity('dataset', index_col='dataset').loc[self.dataset]
            meta = meta.where((pd.notnull(meta)), None)
            meta.topics = meta.topics.fillna('').split(',')
            meta['dataset'] = meta.name
            kwargs.update(meta)

        # Create datapackage.json
        dump_json(path / 'datapackage.json', package.create_datapackage(path, **kwargs))

        log.info('Validating package on disk')
        validate_package(path)
