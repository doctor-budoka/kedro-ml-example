from typing import Any, Dict, List, Optional, Union

from pandas import DataFrame


def add_aggregations_for_multiple_columns(
    df: DataFrame,
    src_columns: List[str],
    groupby_cols: Union[str, List[str]],
    aggregations: List[Dict],
) -> DataFrame:
    """
    For each src_column provided, the aggregations from aggregations are applied to create new columns.

    This function applies the same aggregations to each of the source columns
    """
    for col in src_columns:
        df = df.pipe(add_aggregations_for_column, col, groupby_cols, aggregations)
    return df


def add_aggregations_for_column(
    df: DataFrame,
    src_column: str,
    groupby_cols: Union[str, List[str]],
    aggregations: List[Dict],
) -> DataFrame:
    """
    Adds several aggregation columns for the given source column, each at using the same groupby columns

    An aggregation is given by a dictionary:
    """
    for aggregation in aggregations:
        df = df.pipe(
            add_aggregation_column,
            src_column,
            groupby_cols,
            aggregation["agg_fn"],
            fill=aggregation.get("fillna"),
            name=aggregation.get("name"),
        )
    return df


def add_aggregation_column(
    df: DataFrame,
    src_column: str,
    groupby_cols: Union[str, List[str]],
    agg_fn_name: str,
    fill: Union[float, int] = None,
    name: str = None,
) -> DataFrame:
    """Add a new column gotten from src_column by aggregating over groupby_cols using agg_fn_name"""
    if name is None:
        name = agg_fn_name
    new_col_name = f"{src_column}_{name}"
    df[new_col_name] = df.groupby(groupby_cols)[src_column].transform(agg_fn_name)

    if fill:
        df[new_col_name].fillna(fill, inplace=True)
    return df


def add_diffs_for_columns(
    df: DataFrame,
    src_columns: List[str],
    groupby_cols: Union[str, List[str]],
    periods: List[int],
    fill_val: Optional[Any] = None,
    fill_self: bool = False,
) -> DataFrame:
    """For each column in src_columns, we create new columns by taking the difference over that column for each period"""
    for src_col in src_columns:
        df = df.pipe(
            add_diffs_for_column,
            src_col,
            groupby_cols,
            periods,
            fill_val=fill_val,
            fill_self=fill_self,
        )
    return df


def add_diffs_for_column(
    df: DataFrame,
    src_column: str,
    groupby_cols: Union[str, List[str]],
    periods: List[int],
    fill_val: Optional[Any] = None,
    fill_self: bool = False,
) -> DataFrame:
    """Create new columns from src_column using diff over each period"""
    for period in periods:
        df = df.pipe(
            add_diff_for_column,
            src_column,
            groupby_cols,
            period,
            fill_val=fill_val,
            fill_self=fill_self,
        )
    return df


def add_diff_for_column(
    df: DataFrame,
    src_column: str,
    groupby_cols: Union[str, List[str]],
    period: int = 1,
    fill_val: Optional[Any] = None,
    fill_self: bool = False,
) -> DataFrame:
    """
    We create a new column from src_column by taking the difference over period

    We can fill the null values with a specified value using fill_val or
    using the original column value by setting fill_self to True
    """
    new_col_name = f"{src_column}_diff_{period}"
    df[new_col_name] = df.groupby(groupby_cols)[src_column].diff(period)
    if fill_self or fill_val:
        fill_value = df[src_column] if fill_self else fill_val
        df[new_col_name].fillna(fill_value, inplace=True)
    return df


def fill_values_in_columns(
    df: DataFrame, src_columns: List[str], value: Any
) -> DataFrame:
    """Fills na values for multiple columns"""
    fill_values = {src_col: value for src_col in src_columns}
    return df.fillna(fill_values)
