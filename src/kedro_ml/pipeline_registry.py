"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from kedro_ml.pipelines import (
    create_sub_churn_batch_predict_pipeline,
    create_sub_churn_batch_score_pipeline,
    create_sub_churn_score_pipeline,
    create_sub_churn_standard_features_pipeline,
    create_sub_churn_train_pipeline,
)

BASE_PIPELINE_TYPES = {
    "sub_churn_standard_features": create_sub_churn_standard_features_pipeline,
    "sub_churn_train": create_sub_churn_train_pipeline,
    "sub_churn_score": create_sub_churn_score_pipeline,
    "sub_churn_batch_predict": create_sub_churn_batch_predict_pipeline,
    "sub_churn_batch_score": create_sub_churn_batch_score_pipeline,
}


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """

    def get_pipe_name(name, sub_model):
        return f"{name}_{sub_model}" if sub_model else name

    base_pipelines = {
        get_pipe_name(name, sub_model): pipeline_creator(sub_model=sub_model)
        for name, pipeline_creator in BASE_PIPELINE_TYPES.items()
        for sub_model in [None, "game2"]
    }

    def get_composite_pipeline(pipe_name, sub_model):
        return create_sub_churn_standard_features_pipeline() + BASE_PIPELINE_TYPES[
            pipe_name
        ](sub_model=sub_model)

    composite_pipeline = {
        get_pipe_name(pipe_name + "_from_raw", sub_model): get_composite_pipeline(
            pipe_name, sub_model
        )
        for pipe_name in ["sub_churn_train", "sub_churn_score", "sub_churn_batch_score"]
        for sub_model in [None, "game2"]
    }
    return {**base_pipelines, **composite_pipeline}
