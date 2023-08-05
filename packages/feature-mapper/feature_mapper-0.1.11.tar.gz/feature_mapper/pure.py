"""
The content of this module is for testing purposes (i.e., validation
of production code) only.
"""

import itertools
from collections.abc import Iterable
from warnings import warn

import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal
from scipy import sparse


def assertEqual(a, b):
    if (isinstance(a, Iterable) and not isinstance(a, str)) or \
       (isinstance(b, Iterable) and not isinstance(b, str)):
        assert all(a == b), "{} != {}".format(a, b)
    else:
        assert a == b, "{} != {}".format(a, b)


def make_valid_indicator_matrix(indicator_matrix):

    if sparse.issparse(indicator_matrix):
        indicator_matrix = indicator_matrix.toarray()

    if not isinstance(indicator_matrix, np.ndarray):
        raise ValueError(
            "indicator_matrix: ndarray or sparse matrix expected.")

    # the number of input features per output feature
    cardinalities = indicator_matrix.sum(axis=1)
    ordering = np.argsort(-cardinalities)
    if ordering.tolist() != list(range(len(ordering))):
        print("Invalid ordering in indicator matrix.  Fixing that.")
        indicator_matrix = indicator_matrix[ordering, :]

    # remove null-features
    if (cardinalities == 0).sum() > 0:
        print("Removing null-features.")
        nonnullfeatures = np.where(cardinalities[ordering] > 0)[0]
        indicator_matrix = indicator_matrix[nonnullfeatures, :]

    # remove duplicates
    indicator_matrix = pd.DataFrame(indicator_matrix).drop_duplicates().values

    return indicator_matrix


class PureMapper:
    """
    This is the pure python mapper.

    It transforms one feature set into anther feature set using
    indicator_matrix.
    """
    def __init__(self, indicator_matrix):
        """
        indicator_matrix : ndarray,
                           shape = (# output features, # input features)
        A dense matrix, indicating the mapping from input to output features.
        The mapping will be done using the row-ordering of this matrix.
        """
        self.indicator_matrix = make_valid_indicator_matrix(indicator_matrix)

        # the number of input features per output feature
        self.cardinalities = indicator_matrix.sum(axis=1)

        # warn if the output features are not sorted by cardinality,
        # as is required for successful mapping
        sorted_cardinaltities = list(self.cardinalities)
        sorted_cardinaltities.sort(reverse=True)
        if sorted_cardinaltities != list(self.cardinalities):
            warn("Cardinalities not properly (i.e., descendingly) sorted."
                 "You will get unexpected results.")

    def _map_row(self, X, recline_features, row):
        """
        Map transactions in row (of sparse matrix X) onto itemsets.

        Parameters
        ----------
        X : sparse matrix, shape = (# transactions, # input features)

        cardinalities : 1d-array, shape = (# output features, )

        recline_features : array
            Indices of reclined features, i.e. features that are
            always available for mapping.

        row : int
            The index of the row of X to map.
        """
        indicator_matrix = self.indicator_matrix
        cardinalities = self.cardinalities

        # init. output (a single matrix row)
        # remapped_features = np.zeros((1, itemsets_df.shape[0]), dtype=bool)
        remapped_features = []

        # return copy of row as flat ndarray
        t = X.getrow(row).toarray().ravel()

        not_reclined_mask = np.array([
            False if idx in recline_features else True for idx in range(len(t))
        ])

        Ntomap = t.sum()

        # identify itemset candidates via 'reverse-lookup' in
        # the indicator matrix
        cand = np.any(indicator_matrix[:, np.flatnonzero(t)], axis=1)

        # remove candidates of too big cardinality
        cand = np.bitwise_and(cand, cardinalities <= Ntomap)

        for c in np.where(cand)[0]:

            diags_for_candidate = indicator_matrix[c, :]
            if (np.bitwise_and(diags_for_candidate,
                               t) == diags_for_candidate).all():
                remapped_features.append((row, c))
                diags_for_candidate = np.bitwise_and(diags_for_candidate,
                                                     not_reclined_mask)
                t[np.flatnonzero(diags_for_candidate)] = False

        return remapped_features

    def remap_rows(self, X):

        if not isinstance(X, sparse.spmatrix):
            X = sparse.csr_matrix(X)

        if X.dtype != np.int8:
            raise ValueError("X: np.int8 dtype required.")

        nRows = X.shape[0]

        remapped_features = [self._map_row(X, [], row) for row in range(nRows)]
        N_remapped_samples = len(remapped_features)
        N_remapped_features = self.indicator_matrix.shape[0]

        print("assembling sparse matrix from remapped features...")
        mapping_result = list(itertools.chain.from_iterable(remapped_features))
        if len(mapping_result) == 0:
            warn("No data in mapping result.")
            return sparse.coo_matrix(([], ([], [])),
                                     shape=(X.shape[0], N_remapped_features))

        rows, cols = zip(*mapping_result)
        data = np.ones((len(rows), ), dtype=bool)
        remapped_features = sparse.coo_matrix(
            (data, (rows, cols)),
            shape=(N_remapped_samples, N_remapped_features))
        print("  [shape: {}, with {} nonzero elements]".format(
            remapped_features.shape, remapped_features.nnz))
        assert remapped_features.count_nonzero() == remapped_features.nnz

        return remapped_features

    def _remap_input_feature(self,
                             mat,
                             feature_supports,
                             feat_idx,
                             debug=False):
        """
        Remap a single output feature with index feat_idx onto other
        features in the order given by indicator matrix.

        Updated versions of mat and feature_supports are returned.
        We exclude remap destinations for reclined input features.
        """
        assert sparse.isspmatrix_dok(mat)

        result = sparse.find(mat.getcol(feat_idx))
        concerned_rows = result[0]
        values = result[2]
        assert all(values == 1)

        if debug:
            print("Removing {} obs from feature {}".format(
                len(concerned_rows), feat_idx))

        mat[concerned_rows, feat_idx] = False

        feature_supports[feat_idx] -= len(concerned_rows)

        # remap diagnoses (if possible)
        # diags_to_map = frozenset(feature_names[feat_idx].split('_'))
        diags_to_map = frozenset(
            np.where(self.indicator_matrix[feat_idx, :])[0])

        nOut, nIn = self.indicator_matrix.shape

        # if we only have a single feature, we are done
        if len(diags_to_map) == 1:
            # assertEqual(feature_names[feat_idx], list(diags_to_map)[0])
            return mat, feature_supports

        counter = 0
        while diags_to_map:
            if debug:
                print("diags_to_map: ", diags_to_map)

            for i in range(feat_idx + 1, nOut):
                # feat_diags = frozenset(feature_names[i].split('_'))
                feat_diags = frozenset(
                    np.where(self.indicator_matrix[i, :])[0])
                if all(
                        map(lambda feat_diag: feat_diag in diags_to_map,
                            feat_diags)):

                    mat[concerned_rows, i] = True
                    feature_supports[i] += len(concerned_rows)
                    # if debug:
                    #     print("mapped {} patients from feature {} [{}]"
                    #           " onto {} [{}]".format(
                    #               len(concerned_rows), feat_idx,
                    #               feature_names[feat_idx], i,
                    #               feature_names[i]))
                    diags_to_map = diags_to_map - feat_diags
                    break

            break
            counter += 1
            if counter > 100:
                raise RuntimeError("Too many iterations.")

        if debug:
            assert_array_equal(feature_supports,
                               np.squeeze(np.asarray(mat.sum(axis=0))))

        return mat, feature_supports

    def remap_rows_smin(self, X, smin, debug=True):

        if not isinstance(X, sparse.spmatrix):
            X = sparse.csr_matrix(X)

        if X.dtype != np.int8:
            raise ValueError("X: np.int8 dtype required.")

        nOut, nIn = self.indicator_matrix.shape
        assert X.shape[1] == nIn

        mf = self.remap_rows(X)

        # remove features that have support < smin to features
        # somewhere lower in the feature priority list, until no more
        # remapping needs to be done
        feature_supports = np.squeeze(np.asarray(mf.sum(axis=0)))
        feature_mask = feature_supports == 0
        f_idx, f_supp = next(
            filter(
                lambda idx_supp: (not feature_mask[idx_supp[0]] \
                                  and 0 < idx_supp[1] < smin),
                enumerate(feature_supports)), (None, None))

        print("Remapping features.")
        mf_dok = mf.todok()
        while f_idx is not None:

            # f_name = self.feature_names[f_idx]
            f_name = str(f_idx)
            assert f_supp == feature_supports[f_idx]
            if debug:
                print("Removing feature {} (support = {} [<{}])...".format(
                    f_name, f_supp, smin))

            # for each patient, find another set of features to be
            # mapped (this does not change the dimensions of the
            # involved data structures)
            mf, feature_supports = \
                self._remap_input_feature(
                    mf_dok,
                    feature_supports,
                    f_idx,
                    debug=debug)

            feature_mask[f_idx] = True

            assertEqual(mf[:, f_idx].sum(), 0)
            assertEqual(feature_supports[f_idx], 0)

            assert len(feature_supports) == nOut
            assert mf.shape[1] == len(feature_supports)

            f_idx, f_supp = next(
                filter(
                    lambda idx_supp: (not feature_mask[idx_supp[0]]  \
                                      and 0 < idx_supp[1] < smin),
                    enumerate(feature_supports)), (None, None))

        return mf
