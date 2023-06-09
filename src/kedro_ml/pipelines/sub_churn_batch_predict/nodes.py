import logging
from datetime import date
from typing import Dict, List

from kedro.pipeline import node
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from kedro_ml.utils.sub_churn_features import (
    add_currency_features,
    produce_general_std_features,
)

log = logging.getLogger(__name__)


def get_transform_predict_batch_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="transform_predict_batch",
        inputs=[
            "sub_data",
            "characters",
            "character_currency",
            "params:sub_churn_batch_predict.date_start",
            "params:sub_churn_batch_predict.date_end",
            f"params:sub_churn_train{sub_model_suffix}.currency_transform_steps",
        ],
        outputs="sub_churn_predict_batch_transformed",
        func=transform_predict_batch,
    )


def transform_predict_batch(
    sub_data: DataFrame,
    characters: DataFrame,
    char_currency: DataFrame,
    date_start: date,
    date_end: date,
    currency_transform_steps: List[Dict],
) -> DataFrame:
    return produce_general_std_features(sub_data, characters).pipe(
        add_currency_features,
        char_currency,
        date_start,
        date_end,
        currency_transform_steps,
    )


def get_predict_transformed_batch_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="predict_transformed_batch",
        inputs=[
            "sub_churn_predict_batch_transformed",
            "sub_churn_fitted_pipeline",
            f"params:sub_churn_train{sub_model_suffix}.target",
        ],
        outputs="sub_churn_predict_batch_predictions",
        func=predict_transformed_batch,
    )


def predict_transformed_batch(
    data: DataFrame,
    fitted_pipeline: Pipeline,
    target_column: str,
) -> DataFrame:
    """Calculates the score from input data and a fitted pipeline and creates the required report"""
    key = data[["char_id", "sub_id", "sub_start_date"]]
    data = data.set_index("char_id", drop=True)
    y_pred = fitted_pipeline.predict_proba(data)
    return key.assign(**{f"{target_column}_pred": y_pred[:, 1]})
