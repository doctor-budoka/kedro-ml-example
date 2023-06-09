from kedro.pipeline import Pipeline, pipeline

from .nodes import get_score_predict_batch_node


def create_pipeline(sub_model=None, **kwargs) -> Pipeline:
    return pipeline([get_score_predict_batch_node(sub_model=sub_model)])
