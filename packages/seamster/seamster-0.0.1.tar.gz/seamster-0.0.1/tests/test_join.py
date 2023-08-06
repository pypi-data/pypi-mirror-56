import numpy as np
import pandas as pd
import pytest

from .context import JoinSide

from .context import BasicJoin, NameZipJoin, Join, NameZipEntTypeJoin

test_vocab = {
    "mcd": 20,
    "cdo": 6,
    "don": 7,
    "ona": 25,
    "nal": 22,
    "ald": 2,
    "lds": 17,
    "bur": 4,
    "urg": 33,
    "rge": 29,
    "ger": 11,
    "er ": 10,
    "r k": 28,
    " ki": 0,
    "kin": 16,
    "ing": 14,
    "wen": 35,
    "end": 9,
    "ndy": 23,
    "dys": 8,
    "sub": 30,
    "ubw": 31,
    "bwa": 5,
    "way": 34,
    "bli": 3,
    "lim": 18,
    "imp": 13,
    "mpi": 21,
    "pie": 26,
    "ies": 12,
    "qui": 27,
    "uiz": 32,
    "izn": 15,
    "zno": 36,
    "nos": 24,
    "mac": 19,
    "acd": 1,
}


def test_abc_error_for_unimplementedbase():
    class TestJoin(Join):
        pass

    with pytest.raises(TypeError):
        assert TestJoin()


def test_create_tfidf_from_join_sides():
    js_a = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=np.array([1, 2, 3]),
                entity_names=np.array(["McDonalds", "Burger King", "Wendys"]),
            )
        ),
        source="a",
        id_field="ids",
        entity_name_field="entity_names",
    )
    js_b = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=np.array([1, 2, 3, 4]),
                entity_names=np.array(["Subway", "Blimpies", "Quiznos", "MacDonalds"]),
            )
        ),
        source="b",
        id_field="ids",
        entity_name_field="entity_names",
    )
    bs = BasicJoin(join_sides=(js_a, js_b))
    bs.tfidf_from_join()

    assert js_a.tfidf.shape == (3, 37)
    assert js_b.tfidf.shape == (4, 37)
    assert js_a.vectorizer.vocabulary_ == test_vocab


def test_match_from_join_sides():
    js_a = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=np.array([1, 2, 3]),
                entity_names=np.array(["McDonalds", "Burger King", "Wendys"]),
            )
        ),
        source="a",
        id_field="ids",
        entity_name_field="entity_names",
    )
    js_b = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=np.array([1, 2, 3, 4]),
                entity_names=np.array(["Subway", "Blimpies", "Quiznos", "MacDonalds"]),
            )
        ),
        source="b",
        id_field="ids",
        entity_name_field="entity_names",
    )
    bs = BasicJoin(join_sides=(js_a, js_b))
    bs.match_matrix_from_joinsides(lower_bound=0.1)
    assert round(bs.match_matrix.data[0], 5) == 0.73668


def test_match_df_from_joinsides():
    js_a = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=np.array([1, 2, 3]),
                entity_names=np.array(["McDonalds", "Burger King", "Wendys"]),
            )
        ),
        source="a",
        id_field="ids",
        entity_name_field="entity_names",
    )
    js_b = JoinSide(
        data=pd.DataFrame(
            dict(
                ids=np.array([1, 2, 3, 4]),
                entity_names=np.array(["Subway", "Blimpies", "Quiznos", "MacDonalds"]),
            )
        ),
        source="b",
        id_field="ids",
        entity_name_field="entity_names",
    )
    bs = BasicJoin(join_sides=(js_a, js_b))
    # bs.match_matrix_from_joinsides(lower_bound=0.1)
    df = bs.join(lower_bound=0.1)
    assert df.to_dict(orient="records") == [
        {
            "ids_a": 1,
            "entity_names_a": "McDonalds",
            "source_a": "a",
            "clean_entity_names_a": "mcdonalds",
            "ids_b": 4,
            "entity_names_b": "MacDonalds",
            "source_b": "b",
            "clean_entity_names_b": "macdonalds",
            "similarity": 0.73668,
        }
    ]


def test_entity_name_plus_zip_match_df():
    dict1 = {
        "id": [1, 2, 3, 4],
        "names": [
            "Subway",
            "Blimpies",
            "McDonalds Hamburguesas, Inc.",
            "MacDonalds Hamburgers",
        ],
        "zip": [80238, 80238, 80230, 80238],
    }
    dict2 = pd.DataFrame(
        {
            "id": [5, 6, 7],
            "names": ["McDonalds Hamburgers Inc", "Burger King", "Wendys"],
            "zip": [80238, 80238, 80230],
        }
    )
    js_a = JoinSide(
        data=pd.DataFrame(dict1),
        source="a",
        entity_name_field="names",
        id_field="id",
        zip_field="zip",
    )
    js_b = JoinSide(
        data=pd.DataFrame(dict2),
        source="b",
        entity_name_field="names",
        id_field="id",
        zip_field="zip",
    )
    bs = NameZipJoin(join_sides=(js_a, js_b))
    # bs.match_matrix_from_joinsides(lower_bound=0.1)
    df = bs.join(lower_bound=0.8)
    assert df.to_dict(orient="records") == [
        {
            "id_a": 4,
            "names_a": "MacDonalds Hamburgers",
            "zip_a": 80238,
            "source_a": "a",
            "clean_names_a": "macdonalds hamburgers",
            "id_b": 5,
            "names_b": "McDonalds Hamburgers Inc",
            "zip_b": 80238,
            "source_b": "b",
            "clean_names_b": "mcdonalds hamburgers",
            "similarity": 0.86529,
        }
    ]


def test_entity_name_entity_type_zip_match_df():
    dict1 = {
        "id": [1, 2, 3, 4],
        "names": [
            "Subway",
            "Blimpies",
            "McDonalds Hamburguesas, Inc.",
            "MacDonalds Hamburgers",
        ],
        "zip": [80238, 80238, 80230, 80238],
        "entity_type": ["llc", "llc", "corporation", "corporation"],
    }
    dict2 = pd.DataFrame(
        {
            "id": [5, 6, 7],
            "names": ["McDonalds Hamburgers Inc", "Burger King", "Wendys"],
            "zip": [80238, 80238, 80230],
            "entity_type": ["corporation", "llc", "inc"],
        }
    )
    js_a = JoinSide(
        data=pd.DataFrame(dict1),
        source="a",
        entity_name_field="names",
        id_field="id",
        zip_field="zip",
        entity_type_field="entity_type",
    )
    js_b = JoinSide(
        data=pd.DataFrame(dict2),
        source="b",
        entity_name_field="names",
        id_field="id",
        zip_field="zip",
        entity_type_field="entity_type",
    )
    bs = NameZipEntTypeJoin(join_sides=(js_a, js_b))
    # bs.match_matrix_from_joinsides(lower_bound=0.1)
    df = bs.join(lower_bound=0.1)
    assert df.to_dict(orient="records") == [
        {
            "id_a": 4,
            "names_a": "MacDonalds Hamburgers",
            "zip_a": 80238,
            "entity_type_a": "corporation",
            "source_a": "a",
            "clean_names_a": "macdonalds hamburgers",
            "clean_entity_type_a": "corp",
            "id_b": 5,
            "names_b": "McDonalds Hamburgers Inc",
            "zip_b": 80238,
            "entity_type_b": "corporation",
            "source_b": "b",
            "clean_names_b": "mcdonalds hamburgers",
            "clean_entity_type_b": "corp",
            "similarity": 0.86529,
        }
    ]
