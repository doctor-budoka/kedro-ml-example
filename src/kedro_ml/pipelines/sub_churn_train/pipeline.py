from kedro.pipeline import Pipeline, pipeline

from kedro_ml.pipelines.sub_churn_train.nodes import (
    get_add_currency_features_node,
    get_create_and_train_pipeline_node,
    get_in_sample_score_report_node,
)


def create_pipeline(sub_model=None, **kwargs) -> Pipeline:
    return pipeline(
        [
            get_add_currency_features_node(sub_model=sub_model),
            get_create_and_train_pipeline_node(sub_model=sub_model),
            get_in_sample_score_report_node(sub_model=sub_model),
        ]
    )
