from typing import List

import pandas as pd
import requests

from datasetmaker.onto.manager import _map


def create_info(jdata: List[dict]) -> pd.DataFrame:
    """
    Create dataframe with additional info on MEPs.

    Parameters
    ----------
    jdata
        List of dicts with additional data.
    """
    info = []

    for x in jdata:
        try:
            for y in x['personuppgift']['uppgift']:
                info.append(y)
        except (TypeError, AttributeError):
            continue

    df = pd.DataFrame(info)
    df = df.drop(['intressent_id', 'typ'], axis=1)
    df = df[df.kod != 'en']
    df.uppgift = df.uppgift.apply(lambda x: x[0])
    df.kod = df.kod.replace('sv', 'titlar')
    df = df.pivot_table(index=['hangar_id'],
                        values='uppgift',
                        columns=['kod'], aggfunc=sum)

    df = df.drop(['Övriga webbsidor'], axis=1)

    df = df.rename(columns={
        'Anställningar': 'riksdagen_employments',
        'Bostadsort': 'city',
        'Föräldrar': 'riksdagen_parents',
        'KandiderarINastaVal': 'riksdagen_run_status',
        'Kommunala uppdrag': 'riksdagen_municipal_assignments',
        'Litteratur': 'riksdagen_literature',
        'Officiell e-postadress': 'email',
        'Tjänstetelefon': 'telephone',
        'Uppdrag inom förenings- och näringsliv': 'riksdagen_other_assignments',
        'Uppdrag inom riksdag och regering': 'riksdagen_parl_gov_assignments',
        'Uppdrag inom statliga myndigheter m.m.': 'riksdagen_agency_assignments',
        'Utbildning': 'riksdagen_education',
        'Webbsida': 'url',
        'titlar': 'title',
    })

    return df


def create_members(jdata: List[dict]) -> pd.DataFrame:
    """
    Create dataframe with members of the Swedish Parliament.

    Parameters
    ----------
    jdata
        List of dicts of members.
    """
    info = create_info(jdata)
    df = pd.DataFrame(jdata)
    df = df.drop(['hangar_guid',
                  'sourceid',
                  'intressent_id',
                  'person_url_xml',
                  'bild_url_80',
                  'bild_url_192',
                  'iort',
                  'sorteringsnamn',
                  'personuppdrag',
                  'personuppgift'], axis=1)

    df = df.rename(columns={
        'hangar_id': 'mep_swe',
        'fodd_ar': 'birth.year',
        'kon': 'gender',
        'efternamn': 'last_name',
        'tilltalsnamn': 'first_name',
        'parti': 'party',
        'valkrets': 'constituency',
        'bild_url_max': 'image_url',
    })

    df.gender = df.gender.map({'kvinna': 'female', 'man': 'male', 'okänt': 'unknown'})
    df['birth.year'] = df['birth.year'].replace('0', '')
    df.party = (df.party
                .fillna('np')
                .str.lower()
                .replace('-', 'np')
                .replace('fp', 'l')
                .map(_map('party', 'abbr', 'party', include_synonyms=False)))
    df = df.merge(info, left_on='mep_swe', right_index=True, how='left')

    return df


def create_assignments(jdata: List[dict]) -> pd.DataFrame:
    """
    Create dataframe with assignments for members of the Swedish Parliament.

    Parameters
    ----------
    jdata
        List of dicts of assignments.
    """
    items = [y for x in jdata for y in x['personuppdrag']['uppdrag']]
    df = pd.DataFrame(items)
    df = df.drop(['ordningsnummer',
                  'uppgift',
                  'intressent_id',
                  'typ',
                  'sortering',
                  'organ_sortering',
                  'uppdrag_rollsortering',
                  'uppdrag_statussortering'], axis=1)

    df = df.rename(columns={
        'from': 'start_day',
        'tom': 'end_day',
        'organ_kod': 'riksdagen_agency',
        'hangar_id': 'mep_swe',
        'roll_kod': 'title',
    })

    df.riksdagen_agency = df.riksdagen_agency.str.lower()
    df['riksdagen_assignment'] = (df
                                  .mep_swe.str.cat(df.riksdagen_agency, sep='_')
                                  .str.cat(df.start_day.str[:4], sep='_')
                                  .str.lower())

    codes = get_codes()
    df['riksdagen_agency__name'] = df.riksdagen_agency.map(codes)

    return df


def get_codes() -> dict:
    """Get official codes for Swedish agencies."""
    r = requests.get('http://data.riksdagen.se/sv/koder/?typ=organ&utformat=json')
    codes = pd.DataFrame(r.json()['organ']['organ'])
    codes['kod'] = codes['kod'].str.lower()
    codes = codes.set_index('kod').namn.to_dict()

    codes.update({
        'fp': 'Liberalerna',
        'bou': 'Bostadsutskottet',
        'systembolaget': 'Systembolaget',
        'lu': 'Lagutskottet',
        'kuu': 'Konstitutions- och utrikesutskottet',
        'esk': 'OSSE-delegationen',
        'umju': 'Sammansatta utrikes-, miljö- och jordbruksutskottet',
        'usou': 'Sammansatta utrikes- och socialutskottet',
        'jusou': 'Sammansatta justitie- och socialutskottet,',
        'empa': 'Euro-Mediterranean Parliamentary Assembly',
        'efta': 'Europeiska frihandelssammanslutningen',
    })

    return codes


def get_meps() -> tuple:
    """Get all data related to members of the Swedish Parliament."""
    url = 'http://data.riksdagen.se/personlista/'
    params = {'rdlstatus': 'samtliga', 'utformat': 'json'}
    r = requests.get(url, params=params)
    data = r.json()['personlista']['person']
    members = create_members(data)
    assignments = create_assignments(data)

    mep_props = ['birth.year', 'gender', 'last_name', 'first_name', 'party',
                 'constituency', 'status', 'image_url', 'riksdagen_employments', 'city',
                 'riksdagen_parents', 'riksdagen_run_status',
                 'riksdagen_municipal_assignments', 'riksdagen_literature', 'email',
                 'telephone', 'riksdagen_other_assignments',
                 'riksdagen_parl_gov_assignments', 'riksdagen_agency_assignments',
                 'riksdagen_education', 'url', 'title']
    members.ddf.register_entity('mep_swe', props=mep_props)
    members.ddf.register_entity('gender')
    members.ddf.register_entity('party')

    assignment_props = ['riksdagen_agency', 'status', 'start_day', 'end_day', 'mep_swe', 'title']
    assignments.ddf.register_entity('riksdagen_assignment', props=assignment_props)
    assignments.ddf.register_entity('mep_swe')
    assignments.ddf.register_entity('riksdagen_agency')

    return members, assignments
