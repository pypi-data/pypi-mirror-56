=========
Changelog
=========

Version 0.2
===========

- New `TimeSeriesCrossValidationDataSplitter` which produces a list of splits of temporal data such that each consecutive train set has one more observation and test set one less. This class can be of use in Time Series analysis, where one wants to produce predictions for several steps ahead starting at different dates, in order to assess predictive power of a model by averaging errors across these dates for each specific horizon.
- New `CrossValidationTimeSeriesQualityReport` for cross-validation time series quality reporting. Collects quality metrics when model predictions are in general non-scalar, e.g. for several time steps ahead.
- New `ModelComparisonReport` takes a splitter, a quality report class, and the list of model/data. It calculates quality metrics for each pair and combines this into one single quality report.
- All splitters return a list of at least one split
- `QualityReportArchetype` calculates quality metrics internally through pandas objects. For that end one needs to implement a new method `_calculate_quality_metrics_as_pandas` for each new quality report that takes true and predicted values as pandas objects and returns pandas objects as well. This allows to add as many dimensions to the report as necessary. For example, one may need to compare several models for several KPI's.

Version 0.1
===========

- First release
