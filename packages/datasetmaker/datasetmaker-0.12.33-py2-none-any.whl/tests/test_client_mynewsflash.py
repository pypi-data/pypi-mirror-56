# mypy: allow-untyped-defs

import unittest

import pandas as pd
import pytest

import datasetmaker
from datasetmaker.clients.mynewsflash.countries import identify_countries


def test_identification():
    articles = [
        {
            'text': 'Italiens premiärminister har avgått',
            'expected': ['ita']
        },
        {
            'text': 'I Guinea-Bissau regnar det mer än i Guinea.',
            'expected': ['gin', 'gnb']
        },
        {
            'text': 'Amerikanska stridsflygplan i Syrien.',
            'expected': ['syr', 'usa']
        },
        {
            'text': 'I Burma finns burmesiska växter.',
            'expected': ['mmr', 'mmr']
        },
        {
            'text': 'I Myanmar, d.v.s. Burma, finns burmesiska växter.',
            'expected': ['mmr', 'mmr', 'mmr']
        },
        {
            'text': 'Med Kongo avses Kongo-Kinshasa.',
            'expected': ['cod', 'cod']
        },
        {
            'text': 'Med Kongo avses inte Kongo-Brazzaville.',
            'expected': ['cod', 'cog']
        },
        {
            'text': 'Luxemburgs premiärminister besökte Danmark',
            'expected': ['dnk', 'lux']
        },
        # {
        #     'text': 'Polischef Lena Tysk frias från anklagelserna',
        #     'expected': []
        # },
    ]

    articles = pd.DataFrame(articles)
    articles['identified'] = identify_countries(articles['text'])
    articles['identified'] = articles['identified'].apply(sorted)
    identified = articles['identified'].to_list()
    expected = articles['expected'].to_list()
    assert identified == expected
