import logging

from kedro.pipeline import node
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from kedro_ml.utils.sub_churn_features import add_currency_features
from kedro_ml.utils.scoring import calculate_roc_auc_score

log = logging.getLogger(__name__)


def get_filter_and_transform_scoring_data_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="transform_score_data",
        inputs=[
            "sub_churn_standard_features",
            "character_currency",
            "params:sub_churn_score.date_start",
            "params:sub_churn_score.date_end",
            f"params:sub_churn_train{sub_model_suffix}.currency_transform_steps",
        ],
        outputs="sub_churn_full_features_score",
        func=add_currency_features,
    )


def get_score_report_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="score_report",
        inputs=[
            "sub_churn_full_features_score",
            "sub_churn_fitted_pipeline",
            f"params:sub_churn_train{sub_model_suffix}.target",
        ],
        outputs="score_report",
        func=get_score_report,
    )


def get_score_report(
    data: DataFrame,
    fitted_pipeline: Pipeline,
    target_column: str,
) -> str:
    """Calculates the score from input data and a fitted pipeline and creates the required report"""
    data = data.set_index("char_id", drop=True)

    general_score = calculate_roc_auc_score(data, fitted_pipeline, target_column)
    general_msg = f"General score: {general_score} on {len(data)} characters."

    new_char_data = data.query("is_first_sub")
    if len(new_char_data) > 0:
        new_char_score = calculate_roc_auc_score(
            new_char_data, fitted_pipeline, target_column
        )
        new_char_msg = f"New character score: {new_char_score} on {len(new_char_data)}."
    else:
        new_char_msg = f"No new characters for scoring."

    msg = "\n".join([general_msg, new_char_msg])
    log.info(msg)
    return msg
