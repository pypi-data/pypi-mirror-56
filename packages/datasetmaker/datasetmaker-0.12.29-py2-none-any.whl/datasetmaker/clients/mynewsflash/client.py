import logging
from pathlib import Path
from typing import Any, Tuple, Union

import ddf_utils
import pandas as pd

from .corpus import ArticleDropper
from .countries import identify_countries
from .download import NewsFetcher

from datasetmaker import s3
from datasetmaker.datapackage import DataPackage
from datasetmaker.models import Client
from datasetmaker.onto.manager import _map
from datasetmaker.utils import nice_string, stretch

log = logging.getLogger(__name__)


class MyNewsFlashClient(Client):
    """Client for MyNewsFlash news articles data."""

    _default_ts = pd.Timestamp('2017-01-01T00:00:01+00:00')

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """
        Get news articles.

        Parameters
        ----------
        append_to
            Path to existing datapackage. If supplied, appends only missing days.
        starting_month
            Month to start counting from, format '%Y-%m'
        """
        log.info('Syncing remote data store')
        self._sync_data_store()
        starting_month = kwargs.get('starting_month')

        if kwargs.get('append_to'):
            if starting_month:
                raise ValueError('Cannot pass both starting_month and append_to')
            if not Path(kwargs['append_to']).exists():
                log.info('Downloading remote S3 directory')
                s3.download_dir('datastory', kwargs['append_to'], 'datasets/mynewsflash')
            log.info('Reading timestamp of existing local package')
            ddf_path = Path(kwargs.get('append_to', ''))
            pkg_ts = pd.Timestamp(ddf_utils.package.get_datapackage(ddf_path)['created'])
        elif starting_month:
            pkg_ts = pd.Timestamp(starting_month + '-01T00:00:01+00:00')
        else:
            pkg_ts = self._default_ts

        time_key = f'{str(pkg_ts.year)}-{str(pkg_ts.month).zfill(2)}'
        raw_files = list(s3.list_files_in_s3_directory('datastory',
                                                       'client-data-store',
                                                       suffix='csv'))
        to_process = [x for x in raw_files if Path(x).stem >= time_key]
        log.info(f'Preparing to process {len(to_process)} raw files')
        df = self._identify_countries([s3.read_remote_csv('datastory', x) for x in to_process])

        log.info('Creating articles dataframe')
        articles = self._create_articles(df)

        log.info('Creating country counts dataframe')
        day_counts, week_counts = self._count_countries(df)
        day_counts.ddf.register_entity('country')
        day_counts.ddf.register_datapoints('mynewsflash_swe_media_mentions', ['country', 'day'])
        week_counts.ddf.register_entity('country')
        week_counts.ddf.register_datapoints('mynewsflash_swe_media_mentions', [
                                            'country', 'week'])

        articles.ddf.register_entity('media_org')
        articles.ddf.register_entity('mynewsflash_swe_media_country_mention', props=['country',
                                                                                     'day',
                                                                                     'headline',
                                                                                     'media_org',
                                                                                     'url'])

        self.data = [day_counts, week_counts, articles]
        return self.data

    def _create_articles(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[['headline', 'source', 'indexed', 'url', 'countries']]
        df['day'] = df.indexed.dt.strftime('%Y-%m-%d')
        df = df.drop('indexed', axis=1)
        df = stretch(df,
                     index_col=['day', 'source', 'headline', 'url'],
                     value_col='countries',
                     sep=',')
        df = df.rename(columns={
            'source': 'media_org',
            'countries': 'country',
        })
        df.media_org = df.media_org.str.replace(' - Ekot', '').str.strip()
        df.media_org = df.media_org.map(_map('media_org', 'name', 'media_org'))
        df['mynewsflash_swe_media_country_mention'] = (df.url + df.country).apply(nice_string)
        return df

    def _identify_countries(self, dfs: list) -> pd.DataFrame:
        """
        Identify countries mentioned and drop articles without mentions.

        Parameters
        ----------
        dfs
            List of dataframes
        """
        log.info('Identifying countries in dataframe')
        # Merge dataframes
        for df in dfs:
            df.indexed = pd.to_datetime(df.indexed, utc=True)
        df = pd.concat(dfs, sort=True)

        # Drop unwanted rows and columns
        drop_cols = ['country', 'image', 'language', 'links', 'reference']
        df = df.drop(drop_cols, axis=1)
        dropper = ArticleDropper(drop_duplicates=False)
        df = dropper.transform(df)

        # Identify countries mentioned
        df['countries'] = identify_countries(df.headline + ' ' + df.lead)
        df.countries = df.countries.apply(lambda x: ','.join(set(x)))
        df = df[(df.countries.notnull()) & (df.countries != '')]

        return df

    def _count_countries(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Count number of media mentions in df by country and time period.

        Returns counts by date and year-week.
        """
        df = df[['indexed', 'countries']]
        df = stretch(df, index_col='indexed', value_col='countries', sep=',')
        df['day'] = df.indexed.dt.strftime('%Y-%m-%d')
        df['week'] = df.indexed.dt.week.astype(str).str.zfill(2)
        df['year'] = df.indexed.dt.year.astype(str)

        days = df.groupby(['countries', 'day']).size()
        days = days.to_frame().reset_index()
        days.columns = ['country', 'day', 'mynewsflash_swe_media_mentions']
        days = days.sort_values(['country', 'day'])

        weeks = df.groupby(['countries', 'year', 'week']).size()
        weeks = weeks.to_frame().reset_index()
        weeks.columns = ['country', 'year', 'week', 'mynewsflash_swe_media_mentions']
        weeks.week = weeks.week.astype(str).str.zfill(2)
        weeks.week = weeks.year.astype(str).str.cat(weeks.week, sep='w')
        weeks = weeks.drop('year', axis=1)
        weeks = weeks.sort_values(['country', 'week'])

        return days, weeks

    def _check_latest_raw_ts(self) -> pd.Timestamp:
        """Check timestamp of newest article on S3."""
        log.info('Checking latest raw timestamp')
        files = list(s3.list_files_in_s3_directory(
            'datastory', 'client-data-store/mynewsflash', suffix='csv'))
        latest_file = sorted(files)[-1]
        df = s3.read_remote_csv('datastory', latest_file)
        return pd.to_datetime(df.indexed, utc=True).max()

    def _sync_data_store(self) -> None:
        """Update S3 storage with all articles older than 24 hours."""
        ts = self._check_latest_raw_ts()
        delta = ts.utcnow() - ts
        if delta.days == 0:
            return
        fetcher = NewsFetcher()
        data = fetcher.fetch_period(ts.to_pydatetime(), pd.Timestamp.utcnow())
        df = pd.DataFrame(data)
        df.indexed = pd.to_datetime(df.indexed)
        df['month_year'] = (df.indexed.dt.year.astype(str)
                            .str.cat(df.indexed.dt.month.astype(str).str.zfill(2), '-'))
        for month_year in df.month_year.unique():
            key = f'client-data-store/mynewsflash/{month_year}.csv'
            if s3.obj_exists('datastory', key):
                old = s3.read_remote_csv('datastory', key)
                old.indexed = pd.to_datetime(old.indexed)
                new = pd.concat([old, df[df.month_year == month_year]], sort=True)
            else:
                new = df[df.month_year == month_year]
            new = new.drop_duplicates(subset=['url'])
            new = new.sort_values('indexed')
            new = new.drop('month_year', axis=1)
            s3.write_remote_csv(new, 'datastory', key)
        return

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        log.info('Creating datapackage')
        package = DataPackage(self.data, dataset='mynewsflash')
        package.save(path, append=True, **kwargs)
        log.info('Datapackage successfully created')
