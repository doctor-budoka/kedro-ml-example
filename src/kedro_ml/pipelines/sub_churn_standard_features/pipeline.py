"""
This is a boilerplate pipeline 'sub_churn_standard_features'
generated using Kedro 0.18.6
"""

from kedro.pipeline import Pipeline, pipeline

from .nodes import get_produce_general_std_features_node


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([get_produce_general_std_features_node()])
