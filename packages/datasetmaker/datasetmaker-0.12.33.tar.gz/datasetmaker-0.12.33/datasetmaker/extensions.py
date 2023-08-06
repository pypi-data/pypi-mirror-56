from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd


@pd.api.extensions.register_dataframe_accessor('ddf')
class DDFAccessor:
    """Custom dataframe accessor for keeping track of DDF concepts in frames."""

    def __init__(self, pandas_obj: pd.DataFrame):
        self._validate(pandas_obj)
        self._obj = pandas_obj
        self._entities: List = []
        self._entity_overrides: Dict = {}
        self._properties: Dict = {}
        self._datapoints: List[Tuple] = []
        self._roles: Dict = defaultdict(list)

    @staticmethod
    def _validate(obj: pd.DataFrame) -> None:
        pass

    def _find_entity_cols(self, key: str) -> list:
        """
        Locate columns with domain `key`.

        Parameters
        ----------
        key
            Name of entity.
        """
        out_cols = []
        cols = self._obj.columns.to_list()
        for col in cols:
            components = col.split('.')[-1].split('__')
            if key in components:
                out_cols.append(col)
            else:
                for role in self.roles.get(key, []):
                    if role in components:
                        out_cols.append(col)
        return list(set(out_cols))

    def register_entity(self, key: str, props: list = [], roles: list = []) -> None:
        """
        Register an entity.

        Parameters
        ----------
        key
            Entity identifier.
        props
            Properties of entity.
        roles
            Roles by which the entity is also known.
        """
        if key not in self._entities:
            self._entities.append(key)
        for role in roles:
            self._roles[key].append(role)
        for prop in props:
            self.register_property(prop, key)

    def unregister_entity(self, key: str) -> None:
        """
        Unregister an entity.

        Parameters
        ----------
        key
            Entity identifier.
        """
        if key in self._entities:
            self._entities.remove(key)

    def override_entity(self, key: str, frame: pd.DataFrame) -> None:
        """
        Replace entity data with a custom dataframe.

        Parameters
        ----------
        key
            Entity identifier.
        frame
            Custom dataframe.
        """
        self.register_entity(key)
        self._entity_overrides[key] = frame

    def create_entity_frame(self, key: str) -> Optional[pd.DataFrame]:
        """
        Create a dataframe with entity data.

        Parameters
        ----------
        key
            Entity identifier.
        """
        if key not in self._entities:
            return None

        if key in self._entity_overrides:
            return self._entity_overrides[key]

        cols = self._find_entity_cols(key)

        frames = []
        for col in cols:
            dunder_props = [x for x in self._obj.columns if x.startswith(f'{col}__')]
            frame = self._obj[[col] + dunder_props]
            frame.columns = [x.split('__')[-1].split('.')[-1] for x in frame.columns]
            frames.append(frame)

        df = pd.concat(frames, sort=True)

        if key not in df:
            df[key] = None
        for role in self.roles.get(key, []):
            df[key] = df[key].fillna(df[role])
            df = df.drop(role, axis=1)

        if key not in self._properties:
            return df.drop_duplicates(subset=key).dropna(subset=[key]).reset_index(drop=True)

        return (df
                .merge(self._obj[self._properties[key]], left_index=True, right_index=True)
                .drop_duplicates(subset=key)
                .dropna(subset=[key])
                .reset_index(drop=True))

    @property
    def entities(self) -> list:
        """Get registered entities."""
        return self._entities

    def register_property(self, prop: str, entity: str) -> None:
        """
        Register a property of an entity.

        Parameters
        ----------
        prop
            Property identifier.
        entity
            Entity identifier.
        """
        if entity not in self._properties:
            self._properties[entity] = [prop]
        else:
            if prop not in self._properties[entity]:
                self._properties[entity].append(prop)

    def unregister_property(self, prop: str, entity: str) -> None:
        """
        Unregister a property of an entity.

        Parameters
        ----------
        prop
            Property identifier.
        entity
            Entity identifier.
        """
        if entity not in self._properties:
            return
        if prop in self._properties[entity]:
            self._properties[entity].remove(prop)

    @property
    def properties(self) -> dict:
        """Get registered properties."""
        return self._properties

    def register_datapoints(self, measures: Union[str, list], keys: Union[str, list]) -> None:
        """
        Register a datapoints collection.

        Parameters
        ----------
        measures
            Measures/values of the datapoints collection.
        keys
            Keys that uniquely identify the measurements.
        """
        if type(keys) is str:
            keys = [keys]
        if type(measures) is str:
            measures = [measures]
        self._datapoints.append((measures, keys))

    @property
    def datapoints(self) -> list:
        """Get registered datapoints."""
        return self._datapoints

    @property
    def roles(self) -> dict:
        """Get registered roles."""
        return self._roles
