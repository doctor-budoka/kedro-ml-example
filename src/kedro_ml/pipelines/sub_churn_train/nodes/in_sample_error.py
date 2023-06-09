import logging

from kedro.pipeline import node
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from kedro_ml.utils.scoring import calculate_roc_auc_score

log = logging.getLogger(__name__)


def get_in_sample_score_report_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="in_sample_score_report",
        inputs=[
            "sub_churn_full_features_train",
            "sub_churn_fitted_pipeline",
            f"params:sub_churn_train{sub_model_suffix}.target",
        ],
        outputs="in_sample_score_report",
        func=get_in_sample_score_report,
    )


def get_in_sample_score_report(
    data: DataFrame,
    fitted_pipeline: Pipeline,
    target_column: str,
) -> str:
    """Calculates the score from input data and a fitted pipeline and creates the required report"""
    score = calculate_roc_auc_score(
        data.set_index("char_id", drop=True), fitted_pipeline, target_column
    )
    msg = f"In-sample score: {score}"
    log.info(msg)
    return msg
