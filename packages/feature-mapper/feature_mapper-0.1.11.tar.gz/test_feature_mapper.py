import os

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

from feature_mapper import FeatureMapper, map_features, map_features_smin
from feature_mapper.pure import make_valid_indicator_matrix


def eq_spm(spm1, spm2):
    """
    test equality of two (csr) sparse matrices
    """
    return (len(spm1.indices) == len(spm2.indices) \
            and len(spm1.indptr) == len(spm2.indptr) \
            and all(spm1.indices == spm2.indices) \
            and all(spm1.indptr == spm2.indptr) \
            and all(spm1.data == spm2.data))


def assert_eq_spm(spm1, spm2):
    # this way of comparing is much superior to others, becuase it
    # shows exactly the row of the first difference and the
    # differences there
    if not eq_spm(spm1, spm2):
        assert spm1.toarray().tolist() == spm2.toarray().tolist()


def rand_int8_spm(M, N, density=0.001):
    return ((sparse.rand(M, N, density=density, format='csr') > 0).astype(
        np.int8))


@pytest.fixture(scope='session')
def rand_spm():
    """
    Creates a sparse CSR matrix that can have multiple ones per
    row, but also empty rows.
    """
    return rand_int8_spm(100000, 5, 0.001)


@pytest.fixture(scope='session')
def indicator_matrix():
    """
    example matrix to map 5 input features into 4 output featues,
    greedily from top to bottom
    """
    return np.array([[0, 1, 0, 0, 1], \
                     [0, 1, 0, 1, 0], \
                     [0, 0, 1, 0, 0], \
                     [0, 0, 0, 0, 1]])


def test_map_features(rand_spm, indicator_matrix):
    mf0 = map_features_smin(rand_spm, indicator_matrix, 0)
    mf = map_features(rand_spm, indicator_matrix)
    assert_eq_spm(mf, mf0)


def test_map_features_smin(rand_spm):
    """
    test the remapping function of map_features_smin with random inputs
    """
    for rep in range(1):
        print("Rep", rep, "of random map_features_smin test.")
        indicator_matrix = rand_int8_spm(20, 5, 0.1)
        indicator_matrix = make_valid_indicator_matrix(indicator_matrix)
        mf0 = map_features(rand_spm, indicator_matrix)
        smin = int(np.median(mf0.sum(axis=0).tolist()))
        mf_rust = map_features_smin(rand_spm, indicator_matrix, smin)
        # mf_py = PureMapper(indicator_matrix) \
        #     .map_features_smin(rand_spm, smin).tocsr()
        # assert_eq_spm(mf_rust, mf_py)
        assert (np.vectorize(lambda x: x == 0 or x >= smin)(
            mf_rust.sum(axis=0))).all()


def test_FeatureMapper_smin(rand_spm):
    for rep in range(10):
        mm = rand_int8_spm(20, 15, 0.1)  # max 15 columns
        mm = make_valid_indicator_matrix(mm)
        mm_names = list(map(str, range(mm.shape[1])))
        mm_names = np.random.choice(mm_names,
                                    np.random.randint(16),
                                    replace=False)
        obs_names = np.random.choice(list(map(str, range(rand_spm.shape[1]))),
                                     rand_spm.shape[1],
                                     replace=False)
        mf = FeatureMapper().fit(mm, mm_names)
        mf.transform(rand_spm, obs_names)

        out_names = mf.output_names
        assert len(np.unique(out_names)) == len(out_names), \
            "out_names must be unique"


def test_remapping_0(indicator_matrix):
    """
    test the remapping function of map_features with deterministic inputs
    """
    obs = np.array([[1, 1, 1, 1, 1], \
                    [1, 1, 1, 1, 0], \
                    [1, 1, 0, 1, 0], \
                    [1, 0, 0, 1, 0], \
                    [0, 0, 0, 0, 1]], dtype=np.int8)
    mf = map_features(obs, indicator_matrix)
    mf0 = map_features_smin(obs, indicator_matrix, 0)
    assert_eq_spm(mf, mf0)
    # the first observation shall now have the last output-feature
    # assigned instead of the first one
    assert mf.toarray().tolist() == [[True, False, True, False], \
                                     [False, True, True, False], \
                                     [False, True, False, False], \
                                     [False, False, False, False], \
                                     [False, False, False, True]]

    # # also compare with pure python output; FAILS: this is currently
    # # failing because of a bug in the pure Python mapper
    # mf2_py = PureMapper(indicator_matrix).map_features_smin(obs, 2).tocsr()
    # assert_eq_spm(mf2, mf2_py)


def test_remapping_1(indicator_matrix):
    """
    test the remapping function of map_features_smin with deterministic
    inputs
    """
    obs = np.array([[1, 1, 1, 1, 1], \
                    [1, 1, 1, 1, 0], \
                    [1, 1, 0, 1, 0], \
                    [1, 0, 0, 1, 0], \
                    [0, 0, 0, 0, 1]], dtype=np.int8)
    mf2 = map_features_smin(obs, indicator_matrix, 2)
    # the first observation shall now have the last output-feature
    # assigned instead of the first one
    assert mf2.toarray().tolist() == [[False, True, True, True], \
                                      [False, True, True, False], \
                                      [False, True, False, False], \
                                      [False, False, False, False], \
                                      [False, False, False, True]]

    # # also compare with pure python output; FAILS: this is currently
    # # failing because of a bug in the pure Python mapper
    # mf2_py = PureMapper(indicator_matrix).map_features_smin(obs, 2).tocsr()
    # assert_eq_spm(mf2, mf2_py)


def test_remapping_2():
    # here, we test a little more complex example, first obs is the
    # relvant one: it would get out-(0,2) but out-0 has not enough
    # obs., so it must get out-(1,3) instead.
    obs = np.array([[1, 1, 1, 1, 1],\
                    [1, 1, 1, 0, 1],\
                    [1, 1, 0, 1, 0],\
                    [1, 0, 0, 1, 0],\
                    [0, 0, 0, 0, 1],\
                    [1, 1, 1, 0, 0]], dtype=np.int8)
    mm = np.array([[0, 1, 0, 1, 1],\
                   [1, 0, 0, 0, 1],\
                   [1, 0, 1, 0, 0],\
                   [0, 1, 1, 0, 0],\
                   [0, 0, 0, 0, 1]])
    res1 = [[1, 0, 1, 0, 0],\
            [0, 1, 0, 1, 0],\
            [0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 1],\
            [0, 0, 1, 0, 0]]

    assert map_features_smin(obs, mm, 1).toarray().tolist() == res1

    # here, we have enough obs for out-1 (withough looking at obs-0)
    # already:
    res2 = [[0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],\
            [0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 0],\
            [0, 0, 0, 0, 0],\
            [0, 0, 0, 1, 0]]
    assert map_features_smin(obs, mm, 2).toarray().tolist() == res2


# def test_pure(rand_spm, indicator_matrix):
#     mf = PureMapper(indicator_matrix).map_features(rand_spm).tocsr()
#     mf_rust = map_features(rand_spm, indicator_matrix)
#     assert_eq_spm(mf, mf_rust)


def test_mapping_priorities(indicator_matrix):
    obs = np.array([[1, 1, 1, 1, 1], \
                    [1, 1, 1, 1, 0], \
                    [1, 1, 0, 1, 0], \
                    [1, 0, 0, 1, 0]], dtype=np.int8)
    mf = map_features(obs, indicator_matrix)
    assert mf.toarray().tolist() == [[True, False, True, False], \
                                     [False, True, True, False], \
                                     [False, True, False, False], \
                                     [False, False, False, False]]

    # # compare with pure python
    # mf_py = PureMapper(indicator_matrix).map_features(obs).tocsr()
    # assert_eq_spm(mf, mf_py)


if os.path.isfile('examples/infeatures.csv'):

    @pytest.fixture(scope='session')
    def example1():
        return \
            pd.read_csv('examples/infeatures.csv', header=None).values,\
            make_valid_indicator_matrix(
                pd.read_csv('examples/mapping_matrix.csv', header=None).values)

    def test_map_features_example1(example1):
        obs, mm = example1
        mf00 = map_features(obs, mm)
        mf0 = map_features_smin(obs, mm, 0)
        assert_eq_spm(mf00, mf0)
        map_features_smin(obs, mm, 10)

    if os.path.isfile('examples/mapping_matrix.npz'):

        def test_FeatureMapper_example(example1):
            obs, _ = example1
            mm = sparse.load_npz('examples/mapping_matrix.npz')
            mm_col = list(
                map(str.strip,
                    open('examples/mapping_matrix.col').readlines()))
            obs_col = np.random.choice(mm_col, obs.shape[1])
            mf = FeatureMapper().fit(mm, mm_col)
            # here we have underdetermined input features:
            mf.transform(obs, obs_col)


def test_FeatureMapper(indicator_matrix):
    obs_under = np.array([[1, 1, 1, 1], \
                          [1, 1, 1, 1], \
                          [1, 1, 0, 1], \
                          [1, 0, 0, 1]], dtype=np.int8)
    names = ['A', 'B', 'C', 'D', 'E']  # indicator matrix input feaure names
    mf = FeatureMapper().fit(indicator_matrix, names)
    # here we have underdetermined input features:
    mf_out = mf.transform(obs_under, ['A', 'B', 'C', 'D'])
    assert mf_out.toarray().tolist() == [[True, True], \
                                         [True, True], \
                                         [True, False], \
                                         [False, False]]
    assert mf.output_names == ['B_D', 'C']

    # here we have overdetermined input features:
    obs_over = np.array([[1, 1, 1, 1, 1, 1], \
                         [1, 1, 1, 1, 0, 1], \
                         [1, 1, 0, 1, 0, 0], \
                         [1, 0, 0, 1, 0, 1], \
                         [0, 0, 0, 0, 1, 1]], dtype=np.int8)
    mf_out = mf.transform(obs_over, ['A', 'B', 'C', 'D', 'E', 'F'])
    assert mf_out.toarray().tolist() == [[True, False, True, False], \
                                         [False, True, True, False], \
                                         [False, True, False, False], \
                                         [False, False, False, False],
                                         [False, False, False, True]]
    assert mf.output_names == ['B_E', 'B_D', 'C', 'E']

    # a mixed under-det. case
    mf_out = mf.transform(obs_under, ['B', 'E', 'D', 'F'])
    assert mf.output_names == ['B_E', 'B_D', 'E']
    assert mf_out.toarray().tolist() == [[True, False, False], \
                                         [True, False, False], \
                                         [True, False, False], \
                                         [False, False, False]]

    # a mixed over-det. case
    obs_over = np.array([[1, 1, 1, 1, 1, 1], \
                         [1, 1, 1, 1, 0, 1], \
                         [1, 1, 0, 1, 0, 0], \
                         [1, 0, 0, 1, 0, 1], \
                         [0, 0, 0, 0, 1, 1]], dtype=np.int8)
    mf_out = mf.transform(obs_over, ['F', 'B', 'C', 'D', 'E', 'F'])
    assert mf_out.toarray().tolist() == [[True, False, True, False], \
                                         [False, True, True, False], \
                                         [False, True, False, False], \
                                         [False, False, False, False],
                                         [False, False, False, True]]
    assert mf.output_names == ['B_E', 'B_D', 'C', 'E']
