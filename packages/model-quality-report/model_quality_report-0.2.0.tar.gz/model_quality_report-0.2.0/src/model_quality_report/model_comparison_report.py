from collections import OrderedDict
from typing import List, Tuple, Type

import pandas as pd

from model_quality_report.data_splitter_archetype import DataSplitterArchetype
from model_quality_report.model_archetype import ModelArchetype
from model_quality_report.quality_report_archetype import QualityReportArchetype
from model_quality_report.quality_report_error import QualityReportError


class ModelComparisonReport:
    """Model comparison report.

    Takes a splitter, quality report class, and the list of model/data.
    It calculates quality metrics for each pair and combines this into one single quality report.
    The resulting output is later visualized using a template method `catplot`
    which gives a subset of controls over the same method from `seaborn` library.
    """

    def __init__(self, splitter: DataSplitterArchetype, quality_report: Type[QualityReportArchetype],
                 model_and_data: List[Tuple[ModelArchetype, pd.DataFrame, pd.Series, OrderedDict]]):
        """

        :param splitter: splitter that would split the data for each experiment.
        :param quality_report: class that would produce a quality report for each experiment.
        :param model_and_data: list of tuples which contain the model, X data, y data, and ordered dictionary
        with keys being experiment attribute names and values being experiment attributes.
        """
        self._splitter = splitter
        self._quality_report = quality_report
        self._errors = QualityReportError()
        self._experiment_keys = None
        self._model_and_data = model_and_data
        self.lbl_metrics = self._quality_report.lbl_metrics
        self.lbl_metric_value = self._quality_report.lbl_metric_value

    @staticmethod
    def _get_experiment_keys(model_and_data: List[Tuple[ModelArchetype, pd.DataFrame,
                                                        pd.Series, OrderedDict]]) -> tuple:
        """Get experiment keys.

        """
        experiment_keys_all = [tuple(x[-1].keys()) for x in model_and_data]
        if len(set(experiment_keys_all)) > 1:
            raise RuntimeError('Experiment keys are different!')
        else:
            return experiment_keys_all[0]

    def create_quality_report_and_return_dict(self) -> dict:
        """
        Given a list of experiments compute quality reports for each and combine them in one dictionary.

        :return: dict containing the quality report
        """

        self._experiment_keys = self._get_experiment_keys(self._model_and_data)

        results = dict()
        for model, X, y, experiment_id in self._model_and_data:
            quality_report = self._quality_report(model, self._splitter)
            results[experiment_id.values()] = quality_report.create_quality_report_and_return_dict(X, y)

        return results

    def to_frame(self, report: dict) -> pd.DataFrame:
        """Convert quality report (only metrics part) from dictionary format into DataFrame.

        :return: DataFrame containing the quality report

        Example input
        -------------
        {odict_values(['Model', 'a, b']):
        {'metrics': {'explained_variance_score': 0.9498412698412695, 'mape': 0.17777777777777748,
        'mean_absolute_error': 1.0000000000000016, 'mean_squared_error': 1.2400000000000042,
        'median_absolute_error': 0.9999999999999938, 'r2_score': 0.9114285714285711},
        'data':
        {'true': {4: 12, 0: 3, 1: 6},
        'predicted': {4: 13.600000000000007, 0: 3.999999999999994, 1: 5.599999999999996}}},
        odict_values(['Model', 'a']):
        {'metrics': {'explained_variance_score': 0.9921722113502935, 'mape': 0.18730158730158708,
        'mean_absolute_error': 0.9523809523809496, 'mean_squared_error': 1.1428571428571357,
        'median_absolute_error': 1.1428571428571352, 'r2_score': 0.9921722113502935},
        'data':
        {'true': {5: 30, 0: 3, 1: 6},
        'predicted': {5: 28.857142857142865, 0: 4.428571428571427, 1: 5.7142857142857135}}},
        odict_values(['Model', 'b']):
        {'metrics': {'explained_variance_score': 0.9738066567712493, 'mape': 0.15805487639228444,
        'mean_absolute_error': 0.861450692746535, 'mean_squared_error': 0.9574647848032133,
        'median_absolute_error': 0.5770171149144243, 'r2_score': 0.8835515802266363},
        'data':
        {'true': {0: 3, 1: 6, 3: 10},
        'predicted': {0: 2.5085574572127154, 1: 4.484107579462104, 3: 9.422982885085576}}}}

        Example output
        --------------
                            metrics     value  model exogenous
        0  explained_variance_score  0.949841  Model      a, b
        1                      mape  0.177778  Model      a, b
        2       mean_absolute_error  1.000000  Model      a, b
        3        mean_squared_error  1.240000  Model      a, b
        4     median_absolute_error  1.000000  Model      a, b
        5                  r2_score  0.911429  Model      a, b
        0  explained_variance_score  0.992172  Model         a
        1                      mape  0.187302  Model         a
        2       mean_absolute_error  0.952381  Model         a
        3        mean_squared_error  1.142857  Model         a
        4     median_absolute_error  1.142857  Model         a
        5                  r2_score  0.992172  Model         a
        0  explained_variance_score  0.973807  Model         b
        1                      mape  0.158055  Model         b
        2       mean_absolute_error  0.861451  Model         b
        3        mean_squared_error  0.957465  Model         b
        4     median_absolute_error  0.577017  Model         b
        5                  r2_score  0.883552  Model         b

        """
        results = list()
        for experiment_id, model_report in report.items():
            report_df = (self._quality_report.metrics_to_frame(model_report)
                         .assign(**{key: val for key, val in zip(self._experiment_keys, experiment_id)}))
            results.append(report_df)

        return pd.concat(results)
