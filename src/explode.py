from pandas import DataFrame, json_normalize
from typing import Any, Literal


def explode(data: list[dict[str, Any]], column: str, meta: str = "id", errors: Literal["ignore", "raise"] = "ignore", var_name: str="type") -> DataFrame:
    datum: dict[str, Any]

    for datum in data:
        if column not in datum or not isinstance(datum[column], list):
            datum[column] = []

    data_frame: DataFrame = json_normalize(data, column, meta, errors=errors)

    if data_frame.empty:
        return DataFrame()

    data_frame = data_frame.melt(meta, var_name=var_name, value_name=column[:-1])
    data_frame = data_frame.dropna(subset=[column[:-1]])

    return data_frame
