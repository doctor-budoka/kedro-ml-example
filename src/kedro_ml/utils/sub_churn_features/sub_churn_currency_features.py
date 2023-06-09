from datetime import date
from typing import Dict, List

import pandas as pd
from pandas import DataFrame

from kedro_ml.utils.feature_transformations import (
    add_aggregations_for_multiple_columns,
    add_diffs_for_columns,
    fill_values_in_columns,
)

TRANS_TYPE_MAP = {
    "std_aggregations": add_aggregations_for_multiple_columns,
    "differences": add_diffs_for_columns,
    "fill_values": fill_values_in_columns,
}


def add_currency_features(
    data: DataFrame,
    currency_data: DataFrame,
    date_start: date,
    date_end: date,
    transformation_steps: List[Dict],
) -> DataFrame:
    """Joins currency data to the general data and adds extra currency features"""
    data = data.query(f"(sub_start_date >= '{date_start}') and (sub_start_date <= '{date_end}')")
    currency_data = (
        currency_data.query(f"(date <= '{date_end}') and (date >= '{date_start}')")
        .pipe(apply_sub_churn_pipeline_transformations, transformation_steps)
        # We should take only the currency and aggregation data from the latest date we have for a character
        .assign(latest_date=lambda d: d.groupby("char_id")["date"].transform("max"))
        .query("latest_date == date")
        # We don't need the date of the latest data
        .drop(columns=["latest_date", "date"])
    )
    return pd.merge(data, currency_data, on=["char_id"])


def apply_sub_churn_pipeline_transformations(
    df: DataFrame, transformation_steps: List[Dict]
) -> DataFrame:
    """
    Applies transformations for the sub_churn pipeline

    Written specifically to handle the format provided in the configuration for sub_churn_train
    """
    for step in transformation_steps:
        trans_type, details = next(iter(step.items()))
        df = TRANS_TYPE_MAP[trans_type](df, **details)
    return df
