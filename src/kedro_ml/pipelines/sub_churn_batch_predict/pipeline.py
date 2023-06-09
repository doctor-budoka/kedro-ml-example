from kedro.pipeline import Pipeline, pipeline

from .nodes import get_predict_transformed_batch_node, get_transform_predict_batch_node


def create_pipeline(sub_model=None, **kwargs) -> Pipeline:
    return pipeline(
        [
            get_transform_predict_batch_node(sub_model=sub_model),
            get_predict_transformed_batch_node(sub_model=sub_model),
        ]
    )
