import logging
from importlib import import_module
from typing import Dict, List, Tuple

import pandas as pd
from kedro.pipeline import node
from pandas import DataFrame
from sklearn.base import BaseEstimator as Estimator
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from kedro_ml.pipeline_utils import log_seed

log = logging.getLogger(__name__)


def keep_columns_transformer(columns=[]):
    return ColumnTransformer([("keep", "passthrough", columns)], remainder="drop")


CUSTOM_STEPS = {"KeepColumns": keep_columns_transformer}


def get_create_and_train_pipeline_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="create_and_train_pipeline",
        inputs=[
            "sub_churn_full_features_train",
            f"params:sub_churn_train{sub_model_suffix}.target",
            f"params:sub_churn_train{sub_model_suffix}.pipeline_steps",
        ],
        outputs="sub_churn_fitted_pipeline",
        func=create_and_train_pipeline,
    )


@log_seed(log)
def create_and_train_pipeline(
    data: DataFrame,
    target_column: str,
    pipeline_steps: List[Dict],
):
    """
    Creates the pipeline for the model including preprocessing.

    Fits the pipeline and returns fitted model
    """
    steps = []
    for step_spec in pipeline_steps:
        name = step_spec["name"]
        transformer = step_spec["transformer"]
        del step_spec["name"]
        del step_spec["transformer"]
        steps.append(create_pipeline_step(name, transformer, **step_spec))

    pipeline = Pipeline(steps)
    X, y = data.drop(columns=target_column), pd.DataFrame(data[target_column])
    pipeline.fit(X.set_index("char_id", drop=True), y)
    return pipeline


def create_pipeline_step(
    name: str, transformer: str, **kwargs
) -> Tuple[str, Estimator]:
    """Takes a recipe for a step in the pipeline and returns the tuple for that step"""
    return name, get_step_object(transformer)(**kwargs)


def get_step_object(object_name: str) -> Estimator:
    """Gets the object based on the transformer name"""
    if object_name in CUSTOM_STEPS:
        return CUSTOM_STEPS[object_name]
    return import_object(object_name)


def import_object(object_path: str) -> object:
    """Imports an object based on it's import path"""
    path_list = object_path.split(".")
    object_to_import = path_list[-1]
    module_path = ".".join(path_list[:-1])
    module = import_module(module_path)
    return getattr(module, object_to_import)
