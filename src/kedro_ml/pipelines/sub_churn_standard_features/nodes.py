from kedro.pipeline import node

from kedro_ml.utils.sub_churn_features import produce_general_std_features_and_targets


def get_produce_general_std_features_node():
    return node(
        name="produce_general_std_features",
        inputs=["sub_data", "characters", "sub_miss"],
        outputs="sub_churn_standard_features",
        func=produce_general_std_features_and_targets,
    )
