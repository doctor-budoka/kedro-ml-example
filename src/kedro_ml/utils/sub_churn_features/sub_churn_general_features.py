from pandas import DataFrame


def produce_general_std_features_and_targets(
    sub_data: DataFrame,
    characters: DataFrame,
    sub_miss: DataFrame,
) -> DataFrame:
    """Joins the main data sets together and creates initial features"""
    return (
        produce_general_std_features(sub_data, characters)
        .merge(sub_miss, on="sub_id", how="outer")
        .pipe(add_sub_churn_column_and_remove_sub_miss_data)
    )


def produce_general_std_features(sub_data: DataFrame, characters: DataFrame) -> DataFrame:
    """
    Joins the main data sets together and adds features.

    This does not produce the sub_miss and sub_churn columns.
    """
    return (
        sub_data.merge(characters, on="char_id", how="outer")
        .pipe(add_general_data_features)
        .pipe(add_first_sub_features)
    )


def add_general_data_features(data: DataFrame) -> DataFrame:
    """
    Feature engineering for general data, which consists of subscription, character and sub_miss data.
    Various features, including the target `sub_churn',  are added.

    Returns
    ---------
    data: pd.DataFrame
    """
    return data.assign(
        # add character age at the time the subscription started,
        age_at_sub=lambda d: d.sub_start_date.dt.to_period('M').astype(int) - d.creation_date.dt.to_period('M').astype(int),
        # add profit in case of no sub_churn
        profit=lambda d: d.sub_months * d.price,
        # add how long it took to get to class mastery in days
        months_to_mastery=lambda d: (d.creation_date - d.class_mastery_date).dt.days
    )


def add_first_sub_features(df: DataFrame) -> DataFrame:
    """
    Adds columns about the character's first subscription

    Two columns added:
    1. first_sub_date: The date of the character's first subscription
    2. is_first_sub: Indicates whether this is the character's first subscription.
    """
    return df.assign(
        first_sub_date=lambda d: d.groupby("char_id")["sub_start_date"].transform("first"),
        is_first_sub=lambda d: d.first_sub_date == d.sub_start_date,
    )


def add_sub_churn_column_and_remove_sub_miss_data(data: DataFrame) -> DataFrame:
    """This allows us to add the sub_churn column without adding months_missed columns"""
    return data.pipe(add_sub_churn_and_sub_miss_columns).drop(
        columns=["months_missed", "start_date", "end_date"]
    )


def add_sub_churn_and_sub_miss_columns(data: DataFrame) -> DataFrame:
    """Adds columns for how long a character missed their subscription and if they churned"""
    return data.assign(
        months_missed=lambda d: d.end_date.dt.to_period('M').astype(int) - d.start_date.dt.to_period('M').astype(int) + 1,
        # sub_churn is defined to be 3 months or more without paying subscription
        sub_churn=lambda d: (d.months_missed == 3).astype("int"),
    )
