import abc

import pandas as pd
import copy
from typing import Tuple, List, Union

from model_quality_report.data_splitter_archetype import DataSplitterArchetype
from model_quality_report.model_archetype import ModelArchetype
from model_quality_report.quality_report_error import QualityReportError


class QualityReportArchetype(metaclass=abc.ABCMeta):
    """
    Base metaclass for _model quality reports.

    """
    lbl_metrics = 'metrics'
    lbl_data = 'data'
    lbl_true_values = 'true'
    lbl_predicted_values = 'predicted'
    lbl_metric_value = 'value'

    def __init__(self, model: ModelArchetype, splitter: DataSplitterArchetype):

        self._model = copy.deepcopy(model)
        self._splitter = splitter
        self._errors = QualityReportError()

    def _split_data_for_quality_assessment(self, X: pd.DataFrame, y: pd.Series) \
            -> List[Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]]:
        """
        Given features X and target y are split into training and test data.

        :return:
        """
        splits = list()
        validation_error = self._splitter.validate_parameters(X, y)
        if len(validation_error) == 0:
            splits = self._splitter.split(X, y)
        else:
            self._errors.add('Split failed: {}'.format(validation_error))

        return splits

    def _fit(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Fits _model if it has a fit attribute

        :return:
        """
        try:
            self._model.fit(X_train, y_train)
        except (RuntimeError, AttributeError, ValueError) as e:
            self._errors.add(str(e))

    def _predict(self, X_test: pd.DataFrame) -> pd.Series:
        """
        Predicts with _model if it has a predict attribute and returns predictions

        :return:
        """
        predictions = pd.Series()
        try:
            predictions = pd.Series(self._model.predict(X_test), index=X_test.index)
        except (RuntimeError, AttributeError, ValueError) as e:
            self._errors.add(str(e))
        return predictions

    def _true_and_predicted_values_as_dict(self, true_values: Union[pd.Series, pd.DataFrame],
                                           predictions: Union[pd.Series, pd.DataFrame]) -> dict:
        return {self.lbl_true_values: true_values.to_dict(), self.lbl_predicted_values: predictions.to_dict()}

    def create_quality_report_and_return_dict(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """
        Given a _model and a data set a report on _model performance is created.

        :return: dict containing the quality report
        """
        y_test_all = list()
        predictions_all = list()

        if not self._errors.is_empty():
            return dict()

        for X_train, X_test, y_train, y_test in self._split_data_for_quality_assessment(X, y):

            try:
                self._fit(X_train, y_train)
                predictions = self._predict(X_test)
            except (RuntimeError, ValueError) as e:
                self._errors.add(str(e))
                return dict()
            else:
                y_test_all.append(y_test)
                predictions_all.append(predictions)

        return self._create_dict_from_test_values_and_predictions(y_test_all, predictions_all)

    def _create_dict_from_test_values_and_predictions(self, y_trues: List[pd.Series], y_preds: List[pd.Series]) -> dict:
        """Create report from test and predicted values of y.

        :param y_trues: list of true values of y
        :param y_preds: list of predicted values of y
        :return: quality report in dictionary format
        """
        y_trues = self._convert_list_of_data_to_pandas(y_trues, name=self.lbl_true_values)
        y_preds = self._convert_list_of_data_to_pandas(y_preds, name=self.lbl_predicted_values)

        if not y_trues.index.equals(y_preds.index):
            self._errors.add('Test and predictions objects are not aligned!')
            return dict()

        return {self.lbl_metrics: self._calculate_quality_metrics_as_pandas(y_trues, y_preds).to_dict(),
                self.lbl_data: self._true_and_predicted_values_as_dict(y_trues, y_preds)}

    @staticmethod
    @abc.abstractmethod
    def _calculate_quality_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
        """
        Given y_pred and y_true, various metrics are derived and returned as dict.

        :return: dict containing the quality metrics
        """

    @abc.abstractmethod
    def _calculate_quality_metrics_as_pandas(self, y_true: Union[pd.Series, pd.DataFrame],
                                             y_pred: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
        """
        Given y_pred and y_true, various metrics are derived and returned as pandas object.

        :return: Series or DataFrame containing the quality metrics
        """

    @abc.abstractmethod
    def _convert_list_of_data_to_pandas(self, data: List[pd.Series], name: str = None) \
            -> Union[pd.Series, pd.DataFrame]:
        """Convert list of data to pandas object.

        This method is specific to quality report format.
        If a prediction is a scalar, then we return a Series of predictions for each split.
        If a prediction is array-like, e.g. time horizon along its dimension,
        then we return a DataFrame with rows for each split and columns for each horizon.

        :return: either Series or DataFrame depending on the report specifics
        """

    @classmethod
    @abc.abstractmethod
    def metrics_to_frame(cls, report: dict) -> pd.DataFrame:
        """Convert quality report (only metrics part) from dictionary format into DataFrame.

        :return: DataFrame containing the quality report

        Example input
        -------------
        {'metrics':
        {'explained_variance_score': 0.9148351648351651,
        'mape': 0.4388888888888885,
        mean_absolute_error': 6.66666666666666,
        'mean_squared_error': 51.33333333333321,
        'median_absolute_error': 7.999999999999986,
        'r2_score': 0.365384615384617},
        'data':
        {'true': {4: 12, 3: 10, 5: 30},
        'predicted': {4: 20.999999999999993, 3: 12.999999999999998, 5: 37.999999999999986}}}

        Example output
        --------------
                            metrics      value
        0  explained_variance_score   0.914835
        1                      mape   0.438889
        2       mean_absolute_error   6.666667
        3        mean_squared_error  51.333333
        4     median_absolute_error   8.000000
        5                  r2_score   0.365385

        """

    def set_model(self, model: ModelArchetype):
        self._model = model

    def get_model(self) -> ModelArchetype:
        return self._model

    def set_splitter(self, splitter: DataSplitterArchetype):
        self._splitter = splitter

    def get_splitter(self) -> DataSplitterArchetype:
        return self._splitter

    def get_errors(self) -> QualityReportError:
        return self._errors
