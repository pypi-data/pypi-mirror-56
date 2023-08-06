"""
Join Classes for fuzzy joining of two JoinSide objects
"""
from abc import ABC, abstractmethod
import datetime
import re
from typing import Tuple

import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import TfidfVectorizer

from sparse_dot_topn import awesome_cossim_topn

# https://github.com/ing-bank/sparse_dot_topn

from seamster.join_side import JoinSide
from seamster.validate import _validate_zip, _validate_entity_type


class Join(ABC):
    """
    Base Class for the join of two joinsides

    Args:
        join_sides (Tuple[JoinSide, JoinSide]): A tuple of JoinSide objects on which join operations are performed
        vectorizer (TfidfVectorizer): vectorizer to create
    """

    def __init__(
        self, join_sides: Tuple[JoinSide, JoinSide], vectorizer: TfidfVectorizer = None
    ):
        """
        Inits Join Class
        """
        self.join_sides = join_sides
        self.vectorizer = vectorizer
        self.match_matrix = None
        self._validate_sides()

    @abstractmethod
    def _validate_sides(self):
        """
        Private method to validate that both sides have necessary data elements

        Returns:
            None
        """

    # TODO: Implement join method (i.e., equivalent to `how` param in pandas.DataFrame.join
    @abstractmethod
    def join(self) -> pd.DataFrame:
        """
        Workhorse join method for two joinsides

        Returns:
            pd.DataFrame
        """

    def tfidf_from_join(self, n_char=3, **kwargs) -> None:
        """
        given class attribute join_sides, create a tfidf transformation of entity names of both sides to tfidf matrixes

        given two join sides create a tfidf vectorizer and transform the entity names of both sides to tfidf matrixes.
        If js_a/js_b already has a vectorizer it will use this to transform entity name instead.

        Args:
            n_char (int): number of characters with which to tokenize inputs
            **kwargs: additional args to be passed to TfidfVectorizer object instantiation

        Returns:
            None

        """
        js_a = self.join_sides[0]
        js_b = self.join_sides[1]

        print(f"generating tfidf: {datetime.datetime.now()}")
        if self.vectorizer:
            vectorizer = self.vectorizer
        elif js_a.vectorizer:
            vectorizer = js_a.vectorizer
        elif js_b.vectorizer:
            vectorizer = js_b.vectorizer
        else:
            # define custom ngram analyzer to get n-char tokens
            def ngrams(string, n=n_char):
                string = re.sub(r"[,-./]|\sBD", r"", string.lower())
                ngrams = zip(*[string[i:] for i in range(n)])
                return ["".join(ngram) for ngram in ngrams]

            vectorizer = TfidfVectorizer(analyzer=ngrams, **kwargs)

            # create a concatenated version of the input text to fit the vectorizer on
            input_text = np.concatenate(
                (
                    js_a.data[js_a.clean_entity_name_field],
                    js_b.data[js_b.clean_entity_name_field],
                ),
                axis=None,
            )
            vectorizer.fit(input_text)

        # create tfidf for both sides
        for i in [js_a, js_b]:
            i.tfidf = vectorizer.transform(i.data[i.clean_entity_name_field])
            i.vectorizer = vectorizer
        self.vectorizer = vectorizer

    def match_matrix_from_joinsides(
        self,
        ntop: int = 1,
        lower_bound: float = 0.8,
        use_threads: bool = True,
        n_jobs: int = 2,
        n_char: int = 3,
        **kwargs,
    ) -> None:
        """
        given class attribute join_sides, derives a sparse array of cosine similarity calculations

        Args:
            ntop (int): maximum number of matches to be returned
            lower_bound (float): lower bound of cosine similarity score to be used
            use_threads (bool): boolean to use multithread
            n_jobs (int): number of threads
            n_char (int): number of characters with which to tokenize inputs
            **kwargs: additional args to be passed to TfidfVectorizer object instantiation

        Returns:
            None

        """
        self.tfidf_from_join(n_char=n_char, **kwargs)
        print(f"computing matches: {datetime.datetime.now()}")
        matches = awesome_cossim_topn(
            self.join_sides[0].tfidf,
            self.join_sides[1].tfidf.transpose(),
            ntop=ntop,
            lower_bound=lower_bound,
            use_threads=use_threads,
            n_jobs=n_jobs,
        )
        self.match_matrix = matches
        # return matches

    def get_matches_df(self, precision: int = 5, **kwargs) -> pd.DataFrame:
        """
        Creates a joined data frame of the two joinside dataframes

        Args:
            precision (int): number of digits of precision to return for similarity
            **kwargs: additional args to be passed to the `match_matrix_from_joinsides` method

        Returns:
            pd.DataFrame: combined dataframe

        """
        if self.match_matrix is None:
            self.match_matrix_from_joinsides(**kwargs)

        print(f"generating match output: {datetime.datetime.now()}")

        # constrain matrix to matches
        non_zeros = self.match_matrix.nonzero()

        # collect index ids for each side of the join (row = left, col = right)
        sparserows = non_zeros[0]
        sparsecols = non_zeros[1]

        out_dict = {}
        # create left side data

        for col_name in self.join_sides[0].data:
            out_dict[f"{col_name}_{self.join_sides[0].source}"] = (
                self.join_sides[0].data[col_name].ravel()[sparserows.ravel()]
            )

        # create right side data
        for col_name in self.join_sides[1].data:
            out_dict[f"{col_name}_{self.join_sides[1].source}"] = (
                self.join_sides[1].data[col_name].ravel()[sparsecols.ravel()]
            )

        # create similarity output
        similarity = [round(x, precision) for x in self.match_matrix.data]

        out_dict["similarity"] = similarity

        df = pd.DataFrame(out_dict)
        return df


class BasicJoin(Join):
    """
    Join class that provides simple match on entity name
    """

    def _validate_sides(self):
        pass

    def join(self, **kwargs):
        return self.get_matches_df(**kwargs)


class NameZipJoin(Join):
    """
    Join class that matches on entity name and zip code
    """

    def _validate_sides(self):
        _validate_zip(self.join_sides)

    def join(self, **kwargs):
        match_df = self.get_matches_df(**kwargs)
        left_side_zip = f"{self.join_sides[0].zip_field}_{self.join_sides[0].source}"
        right_side_zip = f"{self.join_sides[1].zip_field}_{self.join_sides[1].source}"
        mask = (match_df["similarity"] >= 0.80) & (
            match_df[left_side_zip] == match_df[right_side_zip]
        ) | (match_df["similarity"] >= 0.999)
        return match_df[mask]


class NameZipEntTypeJoin(Join):
    """
    Join Class that matches on zip code, entity type, and entity name
    """

    def _validate_sides(self):
        _validate_zip(self.join_sides)
        _validate_entity_type(self.join_sides)

    def join(self, **kwargs):
        match_df = self.get_matches_df(**kwargs)
        left_side_zip = f"{self.join_sides[0].zip_field}_{self.join_sides[0].source}"
        right_side_zip = f"{self.join_sides[1].zip_field}_{self.join_sides[1].source}"

        left_side_entity_type = (
            f"clean_{self.join_sides[0].entity_type_field}_{self.join_sides[0].source}"
        )
        right_side_entity_type = (
            f"clean_{self.join_sides[1].entity_type_field}_{self.join_sides[1].source}"
        )

        mask = (
            (  # Similarity is greater than .75, zip & entity type match
                (match_df["similarity"] >= 0.75)
                & (match_df[left_side_zip] == match_df[right_side_zip])
                & (match_df[left_side_entity_type] == match_df[right_side_entity_type])
            )
            | (  # Similarity is greater than .85, zip match
                (match_df["similarity"] >= 0.85)
                & (match_df[left_side_zip] == match_df[right_side_zip])
            )  # Identical entity names
            | (match_df["similarity"] >= 0.999)
        )
        return match_df[mask]
