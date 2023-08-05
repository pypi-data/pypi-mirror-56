"""Datasetmaker clients."""

from .esv import ESVClient
from .hdi import HDIClient
from .kolada.client import KoladaClient
from .meps import MEPs
from .mynewsflash.client import MyNewsFlashClient
from .nobel import NobelClient
from .riksdagen.client import RiksdagenClient
from .scb.client import SCBClient
from .sipri import SIPRI
from .skolverket.client import SkolverketClient
from .socialstyrelsen.client import SocialstyrelsenClient
from .tax_justice import TaxJusticeClient
from .unsc import UNSC
from .valforsk import ValforskClient
from .waqi import WAQIClient
from .wikipedia.client import WikipediaClient
from .worldbank.client import WorldBank

available = {
    'esv': ESVClient,
    'hdi': HDIClient,
    'kolada': KoladaClient,
    'meps': MEPs,
    'mynewsflash': MyNewsFlashClient,
    'nobel': NobelClient,
    'riksdagen': RiksdagenClient,
    'scb': SCBClient,
    'sipri': SIPRI,
    'skolverket': SkolverketClient,
    'socialstyrelsen': SocialstyrelsenClient,
    'tax_justice': TaxJusticeClient,
    'unsc': UNSC,
    'valforsk': ValforskClient,
    'waqi': WAQIClient,
    'wikipedia': WikipediaClient,
    'worldbank': WorldBank,
}
