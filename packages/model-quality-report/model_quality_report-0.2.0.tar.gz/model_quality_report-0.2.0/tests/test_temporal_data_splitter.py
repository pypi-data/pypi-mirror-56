import os
import unittest

import pandas as pd

from model_quality_report.temporal_data_splitter import TimeDeltaDataSplitter, SplitDateDataSplitter, \
    TimeSeriesCrossValidationDataSplitter


class TestTimeDeltaDataSplitter(unittest.TestCase):

    def setUp(self):
        __current_dir_path = os.path.dirname(os.path.abspath(__file__))
        test_data = pd.read_pickle(os.path.join(__current_dir_path, 'data/date-value_df.pkl'))
        self.X = test_data.loc[:, ['date']]
        self.X['date'] = pd.to_datetime(self.X['date'])
        self.y = test_data['value']

    def test_splits_according_last_x_days(self):
        magnitude = 30
        unit = 'D'

        splitter = TimeDeltaDataSplitter(date_column_name='date',
                                         time_delta=pd.Timedelta(magnitude, unit=unit))

        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)[0]

        self.assertGreaterEqual(X_test[splitter.date_column_name].min(),
                                self.X[splitter.date_column_name].max() - pd.to_timedelta(arg=magnitude, unit=unit))

        self.assertLessEqual(X_train[splitter.date_column_name].max(),
                             self.X[splitter.date_column_name].max() - pd.to_timedelta(arg=magnitude + 1, unit=unit))

        self.assertSequenceEqual(list(X_train.index), list(y_train.index))
        self.assertSequenceEqual(list(X_test.index), list(y_test.index))

    def test_returns_error_if_time_delta_is_too_large(self):
        splitter = TimeDeltaDataSplitter('date', pd.Timedelta(10000, 'D'))
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('too large' in errors[0])

    def test_returns_error_if_wrong_time_delta_is_provided(self):
        splitter = TimeDeltaDataSplitter('date', 'not_a_time_delta')
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('Timedelta' in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        time_delta = pd.Timedelta(10000, 'D')
        splitter = TimeDeltaDataSplitter('date', time_delta)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual({TimeDeltaDataSplitter.lbl_date_column_name: 'date',
                              TimeDeltaDataSplitter.lbl_time_delta: time_delta},
                             parameters)

    def test_returns_proper_error_in_case_wrong_data_column_name_is_provided(self):
        not_existing_date_column = 'not_existing_date_column'

        splitter = TimeDeltaDataSplitter(not_existing_date_column, pd.Timedelta(10, 'D'))
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('not_existing_date_column' in errors[0])


class TestSplitDateDataSplitter(unittest.TestCase):

    def setUp(self):
        __current_dir_path = os.path.dirname(os.path.abspath(__file__))
        test_data = pd.read_pickle(os.path.join(__current_dir_path, 'data/date-value_df.pkl'))
        self.X = test_data.loc[:, ['date']]
        self.X['date'] = pd.to_datetime(self.X['date'])
        self.y = test_data['value']

    def test_splits_according_last_split_date(self):
        split_date = pd.Timestamp('2017-01-01')
        splitter = SplitDateDataSplitter(date_column_name='date', split_date=split_date)

        X_train, X_test, y_train, y_test = splitter.split(self.X, self.y)[0]

        self.assertGreaterEqual(X_test[splitter.date_column_name].min(), split_date)

        self.assertLessEqual(X_train[splitter.date_column_name].max(), split_date)

        self.assertSequenceEqual(list(X_train.index), list(y_train.index))
        self.assertSequenceEqual(list(X_test.index), list(y_test.index))

    def test_returns_error_if_split_date_too_large(self):
        split_date = pd.Timestamp('2100-01-01')
        splitter = SplitDateDataSplitter('date', split_date)
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(split_date) in errors[0])

    def test_returns_error_if_split_date_too_small(self):
        split_date = pd.Timestamp('1900-01-01')
        splitter = SplitDateDataSplitter('date', split_date)
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(split_date) in errors[0])

    def test_returns_error_if_wrong_timestamp_is_provided(self):
        splitter = SplitDateDataSplitter('date', 'not_a_timestamp')
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('Timestamp' in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        split_date = pd.Timestamp('1900-01-01')

        splitter = SplitDateDataSplitter('date', split_date)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual({SplitDateDataSplitter.lbl_date_column_name: 'date',
                              SplitDateDataSplitter.lbl_split_date: split_date},
                             parameters)

    def test_returns_proper_error_in_case_wrong_data_column_name_is_provided(self):
        not_existing_date_column = 'not_existing_date_column'

        splitter = SplitDateDataSplitter(not_existing_date_column, pd.Timestamp('1900-01-01'))
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('not_existing_date_column' in errors[0])


class TestTimeSeriesCrossValidationDataSplitter(unittest.TestCase):

    def setUp(self):
        __current_dir_path = os.path.dirname(os.path.abspath(__file__))
        test_data = (pd.read_pickle(os.path.join(__current_dir_path, 'data/date-value_df.pkl'))
                     .drop_duplicates(subset=['date'])
                     .assign(date=lambda x: pd.to_datetime(x['date']))
                     .set_index('date')
                     .sort_index())
        self.X = test_data.assign(date=lambda x: x.index)
        self.y = test_data['value']

    def test_correct_number_of_splits(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        self.assertEqual(len(splits), self.X[self.X['date'] >= start_split_date].shape[0] - maximum_horizon)

    def test_split_date_boundaries(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertGreaterEqual(X_test.index.min(), start_split_date)
            self.assertLess(X_train.index.max(), X_test.index.min())

    def test_equality_of_split_x_an_y_indices(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertSequenceEqual(list(X_train.index), list(y_train.index))
            self.assertSequenceEqual(list(X_test.index), list(y_test.index))

    def test_length_of_test_data(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for X_train, X_test, y_train, y_test in splits:
            self.assertEqual(X_test.shape[0], maximum_horizon)
            self.assertEqual(y_test.shape[0], maximum_horizon)

    def test_increment_of_train_data(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        splits = splitter.split(self.X, self.y)

        for split, split_next in zip(splits[:-1], splits[1:]):
            X_train, _, y_train, _ = split
            X_train_next, _, y_train_next, _ = split_next
            self.assertEqual(X_train.shape[0], X_train_next.shape[0] - 1)
            self.assertEqual(y_train.shape[0], y_train_next.shape[0] - 1)

    def test_returns_error_if_no_datetime_index(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)
        errors = splitter.validate_parameters(self.X.reset_index(drop=True), self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('DatetimeIndex' in errors[0])

        errors = splitter.validate_parameters(self.X, self.y.reset_index(drop=True))

        self.assertTrue(len(errors) > 0)
        self.assertTrue('DatetimeIndex' in errors[0])

    def test_returns_error_if_split_date_too_large(self):
        start_split_date = pd.Timestamp('2100-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(start_split_date) in errors[0])

    def test_returns_error_if_split_date_too_small(self):
        start_split_date = pd.Timestamp('1900-01-01')
        maximum_horizon = 10
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(str(start_split_date) in errors[0])

    def test_returns_error_if_maximum_horizon_too_large(self):
        start_split_date = pd.Timestamp('2017-01-01')
        maximum_horizon = 1000
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('maximum_horizon' in errors[0])

    def test_returns_error_if_wrong_timestamp_is_provided(self):
        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date='not_a_timestamp',
                                                         maximum_horizon=10)
        errors = splitter.validate_parameters(self.X, self.y)

        self.assertTrue(len(errors) > 0)
        self.assertTrue('Timestamp' in errors[0])

    def test_parameters_can_be_accessed_by_get_parameters(self):
        start_split_date = pd.Timestamp('1900-01-01')
        maximum_horizon = 10

        splitter = TimeSeriesCrossValidationDataSplitter(start_split_date=start_split_date,
                                                         maximum_horizon=maximum_horizon)

        parameters = splitter.get_parameters()

        self.assertIsInstance(parameters, dict)
        self.assertDictEqual({TimeSeriesCrossValidationDataSplitter.lbl_start_split_date: start_split_date,
                              TimeSeriesCrossValidationDataSplitter.lbl_maximum_horizon: maximum_horizon},
                             parameters)
