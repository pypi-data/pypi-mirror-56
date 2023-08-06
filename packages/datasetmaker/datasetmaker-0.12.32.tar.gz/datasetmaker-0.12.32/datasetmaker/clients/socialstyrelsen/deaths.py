from typing import Tuple

import pandas as pd
import requests


def _parse_interval(val: str) -> str:
    """
    Parse age intervals into DDF compliant format.

    E.g. 0-4 -> [0, 4].
    """
    if val == '85+':
        return '[85, 120]'
    start, end = val.split('-')
    return f'[{start}, {end}]'


def get_age_intervals() -> pd.DataFrame:
    """Get age intervals."""
    df = pd.read_json('https://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/alder')
    df.text = df.text.apply(_parse_interval)
    return df


def get_causes() -> pd.DataFrame:
    """Get causes of death categories."""
    df = pd.read_json('https://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/diagnos',
                      dtype={'grupp': str})
    return df


def parse_causes(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Parse a dataframe with causes of death into chapters, sections, and categories.

    Parameters
    ----------
    df
        Dataframe with causes of death.
    """
    df = df.drop(['info', 'typ'], axis=1)
    # df = df.drop([0, 1])

    chapters = df[(df.id.str.len() == 2) | df.id.isin(['00', 'Alk'])]
    chapters = chapters[['id', 'text']]
    chapters = chapters.rename(columns={'id': 'cod_chapter', 'text': 'name'})

    sections = df[df.id.str.len() == 4]
    sections = sections.drop('kod', axis=1)
    sections = sections.rename(
        columns={'id': 'cod_section', 'text': 'name', 'grupp': 'cod_chapter'})

    categories = df[df.id.str.len() == 3]
    categories = categories.drop('kod', axis=1)
    categories = categories.rename(
        columns={'id': 'cod_category', 'text': 'name', 'grupp': 'cod_section'})
    return chapters, sections, categories


def get_deaths() -> pd.DataFrame:
    """Get all deaths data."""
    frames = []
    finished = False
    url = 'http://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/resultat'
    while finished is False:
        resp = requests.get(url)
        jdata = resp.json()
        data = jdata.get('data')
        frame = pd.DataFrame(data)
        frames.append(frame)
        if jdata.get('nasta_sida'):
            url = jdata.get('nasta_sida')
        else:
            finished = True
    df = pd.concat(frames, sort=True)
    df = df.drop('mattId', axis=1)
    df = df.rename(columns={
        'diagnosId': 'cod',
        'regionId': 'county',
        'alderId': 'age_interval',
        'konId': 'gender',
        'ar': 'year',
        'varde': 'deaths',
    })

    df['deaths'] = df.deaths.astype(int)
    df.county = df.county.astype(str).str.zfill(2)
    df.gender = df.gender.map({1: 'male', 2: 'female', 3: 'all'})

    age_intervals = get_age_intervals()
    age_intervals = age_intervals.set_index('id').text
    df.age_interval = df.age_interval.map(age_intervals)

    chapters, sections, categories = parse_causes(get_causes())

    df['cod_chapter'] = df.cod.apply(lambda x: x if len(x) == 2 else None)
    df['cod_section'] = df.cod.apply(lambda x: x if len(x) == 4 else None)
    df['cod_category'] = df.cod.apply(lambda x: x if len(x) == 3 else None)

    df.ddf.register_entity('county')
    df.ddf.override_entity('cod_chapter', chapters)
    df.ddf.override_entity('cod_section', sections)
    df.ddf.override_entity('cod_category', categories)
    df.ddf.register_entity('gender')
    df.ddf.register_datapoints(measures='deaths', keys=[
                               'county', 'gender', 'cod_chapter', 'age_interval', 'year'])
    df.ddf.register_datapoints(measures='deaths', keys=[
                               'county', 'gender', 'cod_section', 'age_interval', 'year'])
    df.ddf.register_datapoints(measures='deaths', keys=[
                               'county', 'gender', 'cod_category', 'age_interval', 'year'])

    return df
