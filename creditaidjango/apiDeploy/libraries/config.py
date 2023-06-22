# =============================================================================
# file: libraries/config.py
# this file contains the configuration like libraries, machine learning model, and variables
# =============================================================================

# * import libraries
from geopy import distance
import numpy as np
import pandas as pd
import pickle
import random
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    OneHotEncoder,
    MinMaxScaler,
    OrdinalEncoder,
)
from sklearn.compose import ColumnTransformer

# * import machine learning model
model = pickle.load(open("locationMovement3/apiDeploy/model/lasso.pkl", "rb"))

# * Initialize Variables
numerical_feature = ["average_distance"]
ordinal_feature = ["address_stability", "address_suitability"]
address_stability_order = [
    "Sangat tidak stabil",
    "Tidak stabil",
    "Stabil",
    "Sangat stabil",
]
address_suitability_order = ["Tidak Sesuai", "Sesuai", "Sangat Sesuai"]

# * Pipeline for Preprocessing
log_transform = FunctionTransformer(np.log1p)
numerical_transformer = Pipeline(
    steps=[
        ("log_transform", log_transform),
        ("scaler", MinMaxScaler()),
    ]
)
ordinal_transformer = Pipeline(
    steps=[
        (
            "ordinal",
            OrdinalEncoder(
                categories=[address_stability_order, address_suitability_order]
            ),
        ),
    ]
)
pipeline = (
    "column_transformer",
    ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, numerical_feature),
            ("ord", ordinal_transformer, ordinal_feature),
        ]
    ),
)
