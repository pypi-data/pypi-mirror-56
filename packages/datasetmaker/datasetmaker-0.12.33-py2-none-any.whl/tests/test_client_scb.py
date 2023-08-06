import pytest

from .mock.mock_scb_election_data import mock_election_data
from .mock.mock_scb_psu_data import (mock_psu_education_data,
                                     mock_psu_employment_data,
                                     mock_psu_gender_age_data,
                                     mock_psu_gender_background_data,
                                     mock_psu_house_data, mock_psu_income_data,
                                     mock_psu_occupation_data,
                                     mock_psu_region_data, mock_psu_union_data)

import datasetmaker


def mock_get_table_data(url, query, data_format='json'):
    """
    Mock the get_table_data function that handles API requests.
    """
    if url.endswith('ME0104T3'):
        return mock_election_data
    elif url.endswith('Partisympati17'):
        return mock_psu_education_data
    elif url.endswith('Partisympati051'):
        return mock_psu_gender_age_data
    elif url.endswith('Partisympati19'):
        return mock_psu_gender_background_data
    elif url.endswith('Partisympati081'):
        return mock_psu_income_data
    elif url.endswith('Partisympati151'):
        return mock_psu_house_data
    elif url.endswith('Partisympati101'):
        return mock_psu_region_data
    elif url.endswith('Partisympati131'):
        return mock_psu_employment_data
    elif url.endswith('Partisympati141'):
        return mock_psu_union_data
    elif url.endswith('Partisympati12'):
        return mock_psu_occupation_data
    else:
        return None


@pytest.fixture
def scb_data(monkeypatch):
    """
    Monkey patch `get_table_data` with `mock_get_table_data`.
    """
    monkeypatch.setattr('datasetmaker.clients.scb.election_results.get_table_data',
                        mock_get_table_data)
    monkeypatch.setattr('datasetmaker.clients.scb.psu_polls.get_table_data',
                        mock_get_table_data)
    client = datasetmaker.create_client('scb')
    return client.get()


def test_election_data_has_correct_columns(scb_data):
    """
    Test that the election results dataframe has the exact columns as expected.
    """
    data = scb_data[1]
    actual = sorted(data.columns.to_list())
    expected = ['party', 'votes_share', 'votes_tot', 'year']
    assert actual == expected


def test_psu_data_has_correct_columns(scb_data):
    """
    Test that the PSU polls dataframe has the exact columns as expected.
    """
    data = scb_data[0]
    actual = sorted(data.columns.to_list())
    expected = sorted(['day', 'margin_error', 'scb_psu_party_sympathy',
                       'scb_psu_pop_segment', 'scb_psu_pop_segment__category',
                       'scb_psu_pop_segment__name', 'party'])
    assert actual == expected


def test_nyd_has_no_recent_data(scb_data):
    """
    Test that the defunct party NYD has no recent data.
    """
    data = scb_data[0]
    data = data[data.day > '2016-01-01']
    data = data.dropna(subset=['scb_psu_party_sympathy'])
    assert (data.party == 'nyd_swe').any() == False


def test_sample_psu_value(scb_data):
    """
    Test that a specific entry has the expected data.
    """
    row = scb_data[0].query("day == '2008-05-01' & "
                            "party == 'c_swe' & "
                            "scb_psu_pop_segment == 'kon_och_alder_man_65_ar'").iloc[0]
    assert row.scb_psu_party_sympathy == 6.2
    assert row.margin_error == 1.9
