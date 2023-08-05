# __import__('pkg_resources').declare_namespace(__name__)

from .feature_mapper import lib
from .FeatureMapper import FeatureMapper
from .wrapper import map_features, map_features_smin

# initialize Rust (logging)
lib.init()

__all__ = [
    'FeatureMapper',
    'map_features',
    'map_features_smin',
]
