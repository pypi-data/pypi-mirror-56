import os
import random
import unittest

import pandas as pd

from model_quality_report.sorted_data_splitter import SortedDataSplitter


class TestTemporalDataSplitter(unittest.TestCase):

    def setUp(self):
        __current_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.test_data = pd.read_pickle(os.path.join(__current_dir_path, 'data/date-value_df.pkl'))

    def test_date_column_is_properly_split(self):
        date_column_name = 'date'
        value_column_name = 'value'

        X = self.test_data.loc[:, [date_column_name]]
        X[date_column_name] = pd.to_datetime(X[date_column_name])
        y = self.test_data[value_column_name]

        test_size = 0.2
        for ascending in [True, False]:
            splitter = SortedDataSplitter(sortable_column_name=date_column_name, test_size=test_size, ascending=ascending)

            X_train, X_test, y_train, y_test = splitter.split(X, y)[0]

            self.assertAlmostEqual(X_test.shape[0] / X.shape[0], test_size)
            self.assertAlmostEqual(X_train.shape[0] / X.shape[0], 1-test_size)

            self.assertAlmostEqual(y_test.shape[0] / y.shape[0], test_size)
            self.assertAlmostEqual(y_train.shape[0] / y.shape[0], 1 - test_size)

            if ascending:
                self.assertTrue(X_train[date_column_name].max() <= X_test[date_column_name].min())
            else:
                self.assertTrue(X_train[date_column_name].max() >= X_test[date_column_name].min())

    def test_numeric_column_is_properly_split(self):
        sortable_column = 'sortable_column'
        random.seed(2)
        X = pd.DataFrame(data=[random.randint(0, 1000) for i in range(1000)], columns=[sortable_column])
        y = pd.Series(range(1000))

        test_size = 0.5
        splitter = SortedDataSplitter(sortable_column_name=sortable_column, test_size=test_size, ascending=True)

        X_train, X_test, y_train, y_test = splitter.split(X, y)[0]

        self.assertAlmostEqual(X_test.shape[0] / X.shape[0], test_size)
        self.assertAlmostEqual(X_train.shape[0] / X.shape[0], 1-test_size)

        self.assertAlmostEqual(y_test.shape[0] / y.shape[0], test_size)
        self.assertAlmostEqual(y_train.shape[0] / y.shape[0], 1 - test_size)

        self.assertTrue(X_train[sortable_column].max() <= X_test[sortable_column].min())

    def test_validate_parameters_returns_error_if_column_does_not_exist(self):
        not_existing_column = 'not_existing_column'

        random.seed(2)
        X = pd.DataFrame(data=[random.randint(0, 1000) for i in range(1000)], columns=['sortable_column'])
        y = pd.Series(range(1000))

        splitter = SortedDataSplitter(sortable_column_name=not_existing_column, test_size=0.5, ascending=True)
        errors = splitter.validate_parameters(X, y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(not_existing_column in errors[0])

    def test_validate_parameters_returns_error_if_column_can_not_be_sorted(self):
        sortable_column = 'sortable_column'

        random.seed(2)
        X = pd.DataFrame(data=[random.randint(0, 1000) for i in range(1000)], columns=[sortable_column])
        X.loc[0, sortable_column] = 'no_number'
        y = pd.Series(range(1000))

        splitter = SortedDataSplitter(sortable_column_name=sortable_column, test_size=0.5, ascending=True)
        errors = splitter.validate_parameters(X, y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('<' in errors[0])

    def test_validate_parameters_returns_error_if_test_size_is_out_of_bounds(self):
        sortable_column = 'sortable_column'

        random.seed(2)
        X = pd.DataFrame(data=[random.randint(0, 1000) for i in range(1000)], columns=[sortable_column])
        y = pd.Series(range(1000))

        for test_size in [-1, 10]:
            splitter = SortedDataSplitter(sortable_column_name=sortable_column, test_size=test_size, ascending=True)
            errors = splitter.validate_parameters(X, y)

            self.assertTrue(len(errors) > 0)
            self.assertTrue('test_size' in errors[0])
