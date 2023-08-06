# test the ability to create a tf-idf from two dataframes
import re

import numpy as np
import pandas as pd

from seamster.join_side import ___REPLACEMENT_STRINGS___, JoinSide


def test_regex_string_validity():
    for item in ___REPLACEMENT_STRINGS___:
        assert re.sub(item[0], item[1], "test") == "test"


def test_clean_entity_names_with_join_side_misc():

    test_cases = [
        "Test LLC",
        "Test Inc.",
        "Test l.l.c.",
        "Test PC",
        "Test P.C.",
        "Test Ltd.",
        "Test L.L.P.",
    ]

    in_dict = dict(
        ids=np.array([i for i in range(len(test_cases))]),
        entity_names=np.array(test_cases),
    )

    in_data = pd.DataFrame(in_dict)
    js_a = JoinSide(
        source="a", data=in_data, id_field="ids", entity_name_field="entity_names"
    )

    assert np.all(js_a.clean_entity_names == ["test"] * js_a.data.entity_names.shape[0])


def test_clean_entity_names_with_join_side_company():
    test_cases = ["Test Company", "test co"]

    in_dict = dict(
        ids=np.array([i for i in range(len(test_cases))]),
        entity_names=np.array(test_cases),
    )

    in_data = pd.DataFrame(in_dict)
    js_a = JoinSide(
        source="a", data=in_data, id_field="ids", entity_name_field="entity_names"
    )

    assert np.all(js_a.clean_entity_names == ["test"] * js_a.data.entity_names.shape[0])


def test_joinsidedf_creation():
    df1 = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "names": [
                "Subway",
                "Blimpies",
                "McDonalds, Inc.",
                "MacDonalds",
                "Test",
                "MONMOUTH HARDWARE LIMITED LIABILITY COMPANY",
            ],
            "zip": [80238, 80238, 80230, 80238, 80238, 80238],
            "entity_type": [
                "LLC",
                "Corp.",
                "LIMITED PARTNERSHIP",
                "CORPORATION",
                "XXX",
                "LLC",
            ],
        }
    )

    js_a = JoinSide(
        source="a",
        data=df1,
        id_field="id",
        entity_name_field="names",
        entity_type_field="entity_type",
    )
    df1["source"] = "a"
    test_clean_names = [
        "subway",
        "blimpies",
        "mcdonalds",
        "macdonalds",
        "test",
        "monmouth hardware",
    ]
    assert np.all(js_a.data[df1.columns].values == df1.values)

    assert np.all(js_a.clean_entity_names == np.array(test_clean_names))

    assert np.all(js_a.data.clean_names == np.array(test_clean_names))

    assert js_a.entity_type_mapping_dict == {
        "LLC": "llc",
        "XXX": "other",
        "LIMITED PARTNERSHIP": "partner",
        "Corp.": "corp",
        "CORPORATION": "corp",
    }

    assert js_a.data.clean_entity_type.tolist() == [
        "llc",
        "corp",
        "partner",
        "corp",
        "other",
        "llc",
    ]


def test_entity_type_mapping_dict():
    df1 = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6],
            "names": [
                "Subway",
                "Blimpies",
                "McDonalds, Inc.",
                "MacDonalds",
                "Test",
                "MONMOUTH HARDWARE LIMITED LIABILITY COMPANY",
            ],
            "zip": [80238, 80238, 80230, 80238, 80238, 80238],
            "entity_type": [
                "LLC",
                "Corp.",
                "LIMITED PARTNERSHIP",
                "CORPORATION",
                "XXX",
                "LLC",
            ],
        }
    )

    js_a = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=df1.id,
                entity_names=df1.names,
                zip_codes=df1.zip,
                entity_types=df1.entity_type,
            )
        ),
        source="a",
        entity_name_field="entity_names",
        id_field="ids",
        entity_type_field="entity_types",
    )
    assert js_a.entity_type_mapping_dict == {
        "LLC": "llc",
        "XXX": "other",
        "LIMITED PARTNERSHIP": "partner",
        "Corp.": "corp",
        "CORPORATION": "corp",
    }

    assert js_a.data[js_a.clean_entity_type_field].tolist() == [
        "llc",
        "corp",
        "partner",
        "corp",
        "other",
        "llc",
    ]
