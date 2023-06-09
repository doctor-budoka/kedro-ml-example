from kedro.pipeline import node

from kedro_ml.utils.sub_churn_features import add_currency_features


def get_add_currency_features_node(sub_model=None):
    sub_model_suffix = "" if not sub_model else "_" + sub_model
    return node(
        name="add_currency_features",
        inputs=[
            "sub_churn_standard_features",
            "character_currency",
            f"params:sub_churn_train{sub_model_suffix}.date_start",
            f"params:sub_churn_train{sub_model_suffix}.date_end",
            f"params:sub_churn_train{sub_model_suffix}.currency_transform_steps",
        ],
        outputs="sub_churn_full_features_train",
        func=add_currency_features,
    )
