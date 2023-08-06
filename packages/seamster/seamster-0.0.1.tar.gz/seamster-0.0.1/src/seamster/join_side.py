"""
JoinSide class definition to flexibly capture a dataframe for joining, with metadata annotators that facilitate this
"""
import re
import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


___REPLACEMENT_STRINGS___: List[Tuple] = [
    (r"[\.\,'\?]", ""),
    (r"\-", " "),
    (r"service(s)?", "svc"),
    ("construction", "construct"),
    (r"automotive(s)?", "auto"),
    ("community", "comm"),
    (r"enterprise(s)", "enterp"),
    ("management", "mgmt"),
    ("mgmt", "mgmt"),
    (r"solution(s)?", "solution"),
    (r"holding(s)?", "holding"),
    ("center", "ctr"),
    ("systems", "sys"),
    ("northwest", "nw"),
    ("international", "intl"),
    ("insurance", "ins"),
    ("farms", "farm"),
    ("condominium", "condo"),
    ("associates", "assoc"),
    (r"consult(ing|ant(s)?|ancy)", "consulting"),
    ("district", "dist"),
    (r"technolog(ies|y)", "tech"),
    ("maintenance", "maint"),
    (r"electric(al|ian(s)?)?", "elec"),
    (r"propert(ies|y)", "property"),
    (r"investment(s)?", "investment"),
    (r"contract(ing|or)(s)?", "contract"),
    (" and ", " & "),
    (" & ", "&"),
    ("association", "assn"),
    ("incorporated", "inc"),
    ("professional corporation", "pc"),
    (r"professional(s)?", "profess"),
    ("corporation", "corp"),
    ("limited liability company", "llc"),
    ("limited", "ltd"),
    ("company", "co"),
    ("of delaware", ""),
    ("dba", ""),
    (r"^the\s", ""),
    (r"\sthe\s", " "),
    (
        r"(\s(p\.?c|l\.?l\.?(c|p)|ltd|corp|inc|co))+\.?$",
        "",
    ),  # strip off entity type at the end
]

__ENTITY_TYPE_MAPPINGS__: List[Tuple] = [
    ("LIMITED LIABILITY COMPANY", "llc"),
    ("LLC", "llc"),
    ("PROFESSIONAL CORPORATION", "pc"),
    ("PC", "pc"),
    ("CORP", "corp"),
    ("PARTNER", "partner"),
    ("LLP", "partner"),
    ("LP", "partner"),
]

# TODO I think that Location and Entity should be their own disparate classes
#   What I'm struggling with is how to do that given that an entity can have
#   multiple locations
#

# TODO Implement some notion of a transformer middleware that mutates the data upon initialization


class JoinSide:
    """
    Basic Class for joining of two Pandas Dataframes of business entities.

    Args:
            source (str): name of datasource
            data (pd.DataFrame): dataframe of data to be joined
            entity_name_field (str): name of field that contains the entity name
            id_field (str): name of the field that contains the id
            deepcopy (bool): whether to make a deep copy of the data (otherwise will mutate orig df) default=True
            vectorizer (TfidfVectorizer):
            replacement_strings (List[Tuple]): list of replacement string tuples
            entity_type_mappings (List[Tuple]): list of entity type mapping tuples
            **kwargs: additional attributes to be appended to the class
    """

    def __init__(
        self,
        source: str,
        data: pd.DataFrame,
        entity_name_field: str,
        id_field: str,
        deepcopy=True,
        vectorizer: TfidfVectorizer = None,
        replacement_strings: List[Tuple] = None,
        entity_type_mappings: List[Tuple] = None,
        **kwargs,
    ):
        if deepcopy:
            self.data = data.copy()
        else:
            self.data = data
        self.entity_name_field = entity_name_field
        self.id_field = id_field
        self.source = source
        self.data["source"] = source
        self.vectorizer = vectorizer
        self.tfidf = None
        if replacement_strings:
            self.replacement_strings = replacement_strings
        else:
            self.replacement_strings = ___REPLACEMENT_STRINGS___
        if entity_type_mappings:
            self.entity_type_mappings = entity_type_mappings
        else:
            self.entity_type_mappings = __ENTITY_TYPE_MAPPINGS__
        self.__dict__.update(kwargs)
        self.entity_type_mapping_dict = None
        self._clean_up_entity_names()
        self._map_entity_types()

    def _clean_up_entity_names(self):
        """
        Perform regex transformation of entity names to normalize for matching

        Returns:
            None
        """
        self.clean_entity_name_field = f"clean_{self.entity_name_field}"
        print(f"cleaning strings: {datetime.datetime.now()}")
        self.data[self.clean_entity_name_field] = np.copy(
            self.data[self.entity_name_field]
        )
        for item in self.replacement_strings:
            self.data[self.clean_entity_name_field] = self.data[
                self.clean_entity_name_field
            ].apply(lambda a: re.sub(item[0], item[1], a.lower()).strip())

        self.clean_entity_names = self.data[self.clean_entity_name_field].array

    def _create_entity_mapping_lookup(self):
        """
        Create a dictionary to map raw entity type to

        Returns:
            None
        """
        print("creating entity type mapping dict")
        mapping_dict = {}
        for ent_type in set(
            self.data[self.entity_type_field].unique()
        ):  # For each discrete entity type
            ent_type_transform = re.sub(r"\.", "", str(ent_type).upper())
            out_type = "other"  # Default value of "other"
            for mapping in self.entity_type_mappings:  # Overwritten by mapping
                if mapping[0] in ent_type_transform:
                    out_type = mapping[1]
            mapping_dict[ent_type] = out_type
        self.entity_type_mapping_dict = mapping_dict

    def _map_entity_types(self):
        if hasattr(self, "entity_type_field"):
            self.clean_entity_type_field = f"clean_{self.entity_type_field}"
            self._create_entity_mapping_lookup()
            print("mapping entity types")
            self.data[self.clean_entity_type_field] = self.data[
                self.entity_type_field
            ].apply(lambda a: self.entity_type_mapping_dict.get(a, "other"))
