import logging
from datetime import date

from kedro.pipeline import node
from pandas import DataFrame
from sklearn.metrics import roc_auc_score

log = logging.getLogger(__name__)


def get_score_predict_batch_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="score_predict_batch",
        inputs=[
            "sub_churn_standard_features",
            "sub_churn_predict_batch_predictions",
            "params:sub_churn_batch_predict.date_start",
            "params:sub_churn_batch_predict.date_end",
            f"params:sub_churn_train{sub_model_suffix}.target",
        ],
        outputs="predict_batch_score_report",
        func=score_predict_batch,
    )


def score_predict_batch(
    data: DataFrame,
    predictions: DataFrame,
    date_start: date,
    date_end: date,
    target_column: str,
) -> str:
    """Calculates the score from input data and a fitted pipeline and creates the required report"""
    combined = merge_actuals_and_predictions(
        data, predictions, date_start, date_end, target_column
    )
    general_score = roc_auc_score(
        combined[target_column], combined[f"{target_column}_pred"]
    )
    general_msg = f"General score: {general_score} on {len(data)} characters."

    new_char_data = combined.query("is_first_sub")
    if len(new_char_data) > 0:
        new_char_score = roc_auc_score(
            new_char_data[target_column], new_char_data[f"{target_column}_pred"]
        )
        new_char_msg = f"New character score: {new_char_score} on {len(new_char_data)}."
    else:
        new_char_msg = f"No new characters for scoring."

    msg = "\n".join([general_msg, new_char_msg])

    log.info(msg)
    return msg


def merge_actuals_and_predictions(
    data: DataFrame,
    predictions: DataFrame,
    date_start: date,
    date_end: date,
    target_column: str,
) -> DataFrame:
    """Filter the predictions and actuals ready for the scoring function"""
    actuals = data.query(f"sub_start_date <= '{date_end}' and sub_start_date >= '{date_start}'")[
        ["char_id", "sub_id", "is_first_sub", target_column]
    ]
    predicted = predictions.query(
        f"sub_start_date <= '{date_end}' and sub_start_date >= '{date_start}'"
    ).drop(columns=["sub_start_date"])
    return predicted.merge(actuals, on=["char_id", "sub_id"])
