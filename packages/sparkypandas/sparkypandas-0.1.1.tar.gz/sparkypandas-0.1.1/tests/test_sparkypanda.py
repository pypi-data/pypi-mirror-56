#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sparkypanda` package."""


import unittest

from sparkypanda import sparkypanda


class TestSparkypanda(unittest.TestCase):
    """Tests for `sparkypanda` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_create_empty_dataframe(self):
        """Test import."""

        df = sparkypanda.DataFrame()

    def test_create_dataframe_list(self):
        """Test something."""
        data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}

        df = sparkypanda.DataFrame(data)

        self.assertEqual(df.shape, (4, 2))

        df_null = df.select()
        #TODO: spark actually has a weird behaviour cols = 0 and rows = 4
        self.assertEqual(df_null.shape, (0, 0))

        df_all_col = df.select('*')

        self.assertEqual(df_all_col.shape, df.shape)

        df_col_1 = df.select('col_1')

        self.assertEqual(df_col_1.shape,(4,1))

        df_col_2 = df.select('col_2')

        self.assertEqual(df_col_2.shape, (4, 1))

        df_all = df.select('col_2','col_1')

        self.assertEqual(df_all.shape, (4, 2))
        self.assertListEqual(list(df_all.columns.values), ['col_2','col_1'])

        df_all = df.select('col_1', 'col_2')

        self.assertListEqual(list(df_all.columns.values), ['col_1','col_2'])

        with self.assertRaises(sparkypanda.AnalysisException):
            df_wrong_column = df.select('pippo')

