# mypy: allow-untyped-defs

import pathlib
import shutil
import unittest
from datetime import date

import pandas as pd

from datasetmaker.datapackage import DataPackage

tmp_dir = pathlib.Path(__file__).parent / 'tmp'


class TestDatapackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp_dir.mkdir(exist_ok=True)

        c_frame = pd.DataFrame({
            'country': ['swe', 'ita', None, None],
            'esv_allocation': [None, None, '123', '456'],
            'name': [None, None, 'One', 'Two'],
            'sipri_milexp_cap': [10, 20, None, None],
            'esv_budget': [None, None, 50, 60]
        })
        c_frame.ddf.register_entity('country')
        c_frame.ddf.register_entity('esv_allocation')
        c_frame.ddf.register_datapoints(['esv_budget'], ['esv_allocation'])
        cls.c_package = DataPackage(c_frame)

        n_frame = pd.DataFrame({
            'nobel_laureate': ['pocahontas', 'simba', 'ariel'],
            'nobel_laureate__last_name': ['one', 'two', 'three'],
            'birth.city': ['vien', 'amst', 'rome'],
            'birth.city__name': ['Vienna', 'Amsterdam', 'Rome'],
            'birth.date': [date(2010, 1, 1), date(2011, 2, 2), date(2012, 3, 3)],
            'birth.country': ['aus', 'nld', 'ita'],
            'death.country': ['hun', 'dnk', None],
        })
        n_frame.ddf.register_entity('nobel_laureate')
        n_frame.ddf.register_entity('country')
        n_frame.ddf.register_entity('city')
        cls.n_package = DataPackage(n_frame)

        r_frame = pd.DataFrame({
            'country_flow.country_from': ['swe', 'ita'],
            'country_flow.country_to': ['swe', 'ita'],
            'refugees': [1, 2]
        })
        r_frame.ddf.register_entity('country', roles=['country_from', 'country_to'])
        r_frame.ddf.register_datapoints(
            'refugees', ['country_flow.country_from', 'country_flow.country_to'])
        cls.r_package = DataPackage(r_frame)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmp_dir)
        tmp_dir.mkdir()

    def test_c_package_has_concepts(self):
        self.assertTrue(hasattr(self.c_package, 'concepts'))

    def test_n_package_has_concepts(self):
        self.assertTrue(hasattr(self.n_package, 'concepts'))

    def test_c_package_recursively_added_concepts(self):
        self.assertIn('landlocked', self.c_package.concepts.concept.to_list())

    def test_n_package_added_city_concept_from_composite_birth(self):
        self.assertIn('city', self.n_package.concepts.concept.to_list())

    def test_n_package_added_country_concept(self):
        self.assertIn('country', self.n_package.concepts.concept.to_list())

    def test_n_package_added_country_values_from_both_birth_and_death_composites(self):
        self.assertEqual(sorted(self.n_package.entities['country'].country.to_list()),
                         sorted(['aus', 'dnk', 'hun', 'ita', 'nld']))

    def test_n_package_added_composite_birth_concept(self):
        self.assertIn('birth', self.n_package.concepts.concept.to_list())

    def test_n_package_added_composite_death_concept(self):
        self.assertIn('death', self.n_package.concepts.concept.to_list())

    def test_n_package_has_exact_entities(self):
        actual = sorted(list(self.n_package.entities.keys()))
        expected = sorted(
            ['country', 'city', 'nobel_laureate', 'region4', 'region6'])
        self.assertEqual(actual, expected)

    def test_n_package_city_entity_has_name_column(self):
        self.assertIn('name', self.n_package.entities['city'])

    def test_n_package_laureate_entity_has_Last_name_column(self):
        self.assertIn('last_name', self.n_package.entities['nobel_laureate'])

    def test_all_concepts_headers_are_enumerated_in_c_package(self):
        concepts = self.c_package.concepts.concept.to_list()
        columns = self.c_package.concepts.columns.to_list()
        columns.remove('concept')
        columns.remove('concept_type')
        for column in columns:
            self.assertIn(column, concepts)

    def test_c_package_data_has_correct_shape(self):
        self.assertEqual(self.c_package.data.shape, (4, 5))

    def test_c_package_has_country_entity(self):
        self.assertIn('country', self.c_package.entities)

    def test_c_package_has_region4_entity(self):
        self.assertIn('region4', self.c_package.entities)

    def test_c_package_has_region6_entity(self):
        self.assertIn('region6', self.c_package.entities)

    def test_c_package_has_esv_allocation_entity(self):
        self.assertIn('esv_allocation', self.c_package.entities)

    def test_c_package_has_exact_entities(self):
        self.assertEqual(sorted(list(self.c_package.entities.keys())),
                         ['country', 'esv_allocation', 'region4', 'region6'])

    def test_c_package_has_correct_region4_entity_data(self):
        self.assertEqual(self.c_package.entities['region4'].columns.to_list(),
                         ['region4', 'name', 'slug'])

    def test_c_package_has_correct_region4_entity_shape(self):
        self.assertEqual(self.c_package.entities['region4'].shape, (4, 3))

    def test_c_package_has_datapoints(self):
        self.assertIn('ddf--datapoints--esv_budget--by--esv_allocation.csv',
                      self.c_package.datapoints)

    def test_r_package_creates_country_from_roles(self):
        self.assertFalse(self.r_package.entities['country'].empty)

    def test_appending_works(self):
        """
        Test that appending to an existing package appends and does not overwrite.
        """
        df1 = pd.DataFrame({'country': ['swe', 'ita'],
                            'worldbank_sppoptotl': [100, 200]})
        df2 = pd.DataFrame({'country': ['fra'],
                            'worldbank_sppoptotl': [300],
                            'worldbank_sppoptotlfein': [50]})

        df1.ddf.register_datapoints(measures='worldbank_sppoptotl', keys='country')
        df1.ddf.register_entity('country')

        df2.ddf.register_datapoints(measures='worldbank_sppoptotl', keys='country')
        df2.ddf.register_datapoints(measures='worldbank_sppoptotlfein', keys='country')
        df2.ddf.register_entity('country')

        p1 = DataPackage(df1)
        p1.save(tmp_dir / 'pop')

        p2 = DataPackage(df2)
        p2.save(tmp_dir / 'pop', append=True)

        df = pd.read_csv(tmp_dir / 'pop/ddf--datapoints--worldbank_sppoptotl--by--country.csv')
        self.assertEqual(df.shape, (3, 2))
        self.assertTrue(
            (tmp_dir / 'pop/ddf--datapoints--worldbank_sppoptotlfein--by--country.csv').exists())

    def test_not_appending_works(self):
        """
        Test that creating a new package with same path overwrites the old package.
        """
        df1 = pd.DataFrame({'country': ['swe', 'ita'],
                            'worldbank_sppoptotl': [100, 200]})
        df2 = pd.DataFrame({'country': ['fra'], 'worldbank_sppoptotl': [300]})

        df1.ddf.register_datapoints(measures='worldbank_sppoptotl', keys='country')
        df1.ddf.register_entity('country')

        df2.ddf.register_datapoints(measures='worldbank_sppoptotl', keys='country')
        df2.ddf.register_entity('country')

        p1 = DataPackage(df1)
        p1.save(tmp_dir / 'pop_no_append')

        p2 = DataPackage(df2)
        p2.save(tmp_dir / 'pop_no_append', append=False)

        df = pd.read_csv(
            tmp_dir / 'pop_no_append/ddf--datapoints--worldbank_sppoptotl--by--country.csv')
        self.assertEqual(df.shape, (1, 2))

    def test_passing_list(self):
        df1 = pd.DataFrame({'country': ['swe', 'ita'],
                            'worldbank_sppoptotl': [100, 200]})
        df2 = pd.DataFrame({'country': ['fra'], 'worldbank_sppoptotl': [300]})
        df3 = pd.DataFrame({'country': ['tun'], 'worldbank_sppoptotlfein': [300]})

        df1.ddf.register_datapoints(measures='worldbank_sppoptotl', keys='country')
        df1.ddf.register_entity('country')

        df2.ddf.register_datapoints(measures='worldbank_sppoptotl', keys='country')
        df2.ddf.register_entity('country')

        df3.ddf.register_datapoints(measures='worldbank_sppoptotlfein', keys='country')
        df3.ddf.register_entity('country')

        package = DataPackage([df1, df2, df3])
        package.save(tmp_dir / 'pass_list', append=False)

        pop = pd.read_csv(
            tmp_dir / 'pass_list/ddf--datapoints--worldbank_sppoptotl--by--country.csv')
        pop_fe = pd.read_csv(
            tmp_dir / 'pass_list/ddf--datapoints--worldbank_sppoptotlfein--by--country.csv')
        concepts = pd.read_csv(tmp_dir / 'pass_list/ddf--concepts.csv')

        self.assertEqual(pop.shape, (3, 2))
        self.assertEqual(pop_fe.shape, (1, 2))
        self.assertFalse(concepts.concept.duplicated().any())
