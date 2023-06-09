from typing import Tuple

import pandas as pd
from pandas import DataFrame
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline


def calculate_roc_auc_score(
    data: DataFrame,
    fitted_pipeline: Pipeline,
    target_column: str,
) -> float:
    """Calculates error from input data and a fitted pipeline"""
    X, y = split_data_and_target(data, target_column)
    y_pred = fitted_pipeline.predict_proba(X)

    return roc_auc_score(y, y_pred[:, 1])


def split_data_and_target(
    data: DataFrame, target_column: str
) -> Tuple[DataFrame, DataFrame]:
    """Splits a dataframe into X (data) and y (target)"""
    return data.drop(columns=target_column), pd.DataFrame(data[target_column])
