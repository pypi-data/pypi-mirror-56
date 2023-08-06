from typing import List
import pandas as pd

from model_quality_report.data_splitter_archetype import DataSplitterArchetype
from model_quality_report.model_archetype import ModelArchetype
from model_quality_report.quality_metrics import RegressionQualityMetrics
from model_quality_report.quality_report_archetype import QualityReportArchetype


class RegressionQualityReport(QualityReportArchetype):

    def __init__(self, model: ModelArchetype, splitter: DataSplitterArchetype):
        super().__init__(model, splitter)

    @staticmethod
    def _calculate_quality_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
        metric_dict = dict()
        for metric_name in [RegressionQualityMetrics.lbl_explained_variance_score,
                            RegressionQualityMetrics.lbl_mape,
                            RegressionQualityMetrics.lbl_mean_absolute_error,
                            RegressionQualityMetrics.lbl_mean_squared_error,
                            RegressionQualityMetrics.lbl_median_absolute_error,
                            RegressionQualityMetrics.lbl_r2_score]:

            metric_dict[metric_name] = getattr(RegressionQualityMetrics, metric_name)(y_true, y_pred)

        return metric_dict

    @classmethod
    def metrics_to_frame(cls, report: dict) -> pd.DataFrame:
        return (pd.DataFrame.from_dict(report[cls.lbl_metrics], columns=[cls.lbl_metric_value], orient='index')
                .rename_axis(cls.lbl_metrics, axis=0)
                .reset_index())

    def _calculate_quality_metrics_as_pandas(self, y_true: pd.Series, y_pred: pd.Series) -> pd.Series:
        return pd.Series(self._calculate_quality_metrics(y_true, y_pred))

    def _convert_list_of_data_to_pandas(self, data: List[pd.Series], name: str = None) -> pd.Series:
        return pd.Series(data[0])
