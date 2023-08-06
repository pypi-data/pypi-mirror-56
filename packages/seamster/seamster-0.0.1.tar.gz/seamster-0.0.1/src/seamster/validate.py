from typing import Tuple
from seamster.join_side import JoinSide


def _base_validate(joinsides: Tuple[JoinSide, JoinSide], val_name):
    for js in joinsides:
        if hasattr(js, f"{val_name}_field"):
            print(f"joinside {js.source} has {val_name} attr field")
            data_field = getattr(js, f"{val_name}_field")
            if hasattr(js.data, data_field):
                sample = js.data[data_field].tolist()[:5]
                print(f"{val_name} data found in joinside.data attribute:")
                print(sample)
            else:
                raise AttributeError(
                    f"{val_name} field specified in joinside: {js.source},"
                    + " however, no corresponding data found in dataframe given"
                )
        else:
            raise AttributeError(
                f"{val_name} field not specified in joinside: {js.source}\nPlease specify {val_name}_"
                + "field at initialization"
            )


def _validate_zip(joinsides: Tuple[JoinSide, JoinSide]):
    _base_validate(joinsides=joinsides, val_name="zip")


def _validate_entity_type(joinsides: Tuple[JoinSide, JoinSide]):
    _base_validate(joinsides=joinsides, val_name="clean_entity_type")
