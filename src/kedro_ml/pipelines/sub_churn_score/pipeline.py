from kedro.pipeline import Pipeline, pipeline

from .nodes import get_filter_and_transform_scoring_data_node, get_score_report_node


def create_pipeline(sub_model=None, **kwargs) -> Pipeline:
    return pipeline(
        [
            get_filter_and_transform_scoring_data_node(sub_model=sub_model),
            get_score_report_node(sub_model=sub_model),
        ]
    )
