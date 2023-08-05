import numpy as np
from scipy import sparse

from .feature_mapper import ffi, lib


def C(spm):
    return dict(shape=spm.shape,
                indices=(len(spm.indices),
                         ffi.from_buffer('int32_t *', spm.indices)),
                indptr=(len(spm.indptr),
                        ffi.from_buffer('int32_t *', spm.indptr)))


def Py(c):
    return sparse.csr_matrix(
        (np.ones(c.indices.len, dtype=np.bool), \
         ffi.unpack(c.indices.vec, c.indices.len),
         ffi.unpack(c.indptr.vec, c.indptr.len)),
        shape=(c.shape.rows, c.shape.cols))


def sparsify(mat):
    """
    Take any (kind-of boolean) matrix and convert to sparse row matrix.
    """

    if sparse.issparse(mat):
        return mat.tocsr()
    else:
        return sparse.csr_matrix(np.array(mat, dtype=np.int8))


def _v(spm, im):
    spm = C(sparsify(spm))
    im = C(sparsify(im))
    assert spm['shape'][1] == im['shape'][1],\
        "Number of columns of in-feature and mapping matrices must match."
    return spm, im


def map_features(spm, im):
    return Py(lib.remap_rows(*_v(spm, im)))


def map_features_smin(spm, im, smin):
    return Py(lib.remap_rows_smin(*_v(spm, im), smin))
