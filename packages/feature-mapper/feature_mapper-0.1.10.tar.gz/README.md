[![Build Status](https://travis-ci.org/complexity-science-hub/feature-mapper.svg?branch=master)](https://travis-ci.org/complexity-science-hub/feature-mapper)

# Synopsis

Python module (using Rust) to transform a binary observation-feature1
matrix into a binary observation-feature2 matrix.

This is done by greedily applying a binary feature2-feature1 matrix
from top to bottom.


# Algorithm

Inputs:

* an OxM binary input feature matrix.
  row = obseration, column = input feature.

* an NxM binary "translation" or "mapping" matrix;
  row = output feature.  column = input feature.

Output:

* an OxN binary output feature matrix;
  row = output feature.  column = output feature.

Two procedures and a helper class are made available:

    from feature_mapper import map_features, map_features_smin
    from feature_mapper import FeatureMapper

The translation/mapping is performed, as follows (both variants).
Here the activity diagrams:

![activity diagramm of map-features](docs/feature-mapping-activity-0.png)

![activity diagramm of map-feature-smins](docs/feature-mapping-activity-1.png)

The variant `map_features_smin` ensures, that all output features have
at least `smin` observations.

`FeatureMapper` helps by providing a wrapper that can match column
names of the input observation matrix and the mapping matrix.  It also
computes column names the mapped output features by combinding
corresponding input feature names with underscore.  Usage example:

    from feature_mapper import FeatureMapper

    fm = FeatureMapper().fit(mapping_matrix, mapping_matrix_column_names)
    obs_out_features = fm.transform(obs_in_features, in_feature_names)
    out_feature_names = fm.output_names


All matrices are internally processed as scipy.sparse.csr_matrix.


# Install

First, you need to install Rust, e.g. using `wget`:

    wget -O - https://sh.rustup.rs | sh -s

or see https://rustup.rs/


## via pip

    pip install feature-mapper


## via poetry

    poetry add feature-mapper


## via repo-clone (using pyenv)

    git clone https://github.com/complexity-science-hub/feature-mapper.git
    cd feature-mapper

A fresh installation of Python can (and probably should) be obtained via

* installing `pyenv`: https://github.com/pyenv/pyenv

Then (using `fish`):

    pyenv install (cat .python-version)
    pip install -U pip
    pip install maturin
    pip install tox

Build and run tests (takes a few minutes):

    tox

If all is well, install:

    pip install . -v


## License

https://www.gnu.org/licenses/gpl-3.0.html
