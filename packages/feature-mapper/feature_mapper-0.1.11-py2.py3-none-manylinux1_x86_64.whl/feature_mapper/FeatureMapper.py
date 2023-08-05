import numpy as np
import numpy_indexed as npi
import pandas as pd
from scipy import sparse

from .wrapper import map_features, map_features_smin


class FeatureMapper:
    def __init__(self):
        pass

    def fit(self, mapping_matrix, column_names):
        if sparse.issparse(mapping_matrix):
            self.mm = mapping_matrix.toarray()
        else:
            self.mm = np.array(mapping_matrix)
        self.mm_colnames = np.array(column_names)
        return self

    def transform(self, input_obs, column_names, *, smin=None):
        column_names = np.array(column_names)
        both_cols = npi.intersection(column_names, self.mm_colnames)
        obs_cols = npi.indices(column_names, both_cols)
        mm_cols = npi.indices(self.mm_colnames, both_cols)
        obs = input_obs[:, obs_cols]
        mm = self.mm[:, mm_cols]

        # the columns that did not make it
        not_mm_cols = npi.indices(self.mm_colnames,
                                  npi.difference(self.mm_colnames, both_cols))

        # we can only work with rows that have not any "1"
        mm = mm[np.where(self.mm[:, not_mm_cols].sum(axis=1) == 0)[0], :]

        # clearing out "empty" rows
        mm_nonzero_rows = np.where(mm.sum(axis=1))[0]
        mm = mm[mm_nonzero_rows, :]

        # clearing out duplicate rows (out-features)
        mm = pd.DataFrame(mm).drop_duplicates().values

        # generate output names
        self.output_names = [
            '_'.join(map(lambda j: both_cols[j],
                         np.where(mm[row, :])[0]))
            for row in range(mm.shape[0])
        ]

        if smin is None:
            res = map_features(obs, mm)
        else:
            res = map_features_smin(obs, mm, smin)

        return res
