import pandas as pd
import numpy as np
import joblib
import pandas_profiling
from math import *

# plot
import matplotlib.pyplot as plt
import seaborn as sns

# prep
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

# metrics
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import roc_auc_score as auc
from sklearn.metrics import accuracy_score as acc

# models
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Lasso, RidgeCV

from xgboost.sklearn import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor
from lightgbm.sklearn import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor

from xgboost.sklearn import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from lightgbm.sklearn import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier

import lightgbm as lgb
import catboost as cat

# misc
from IPython.core.display import display, HTML
import time

import cquai_ml
import gc
import warnings

warnings.filterwarnings("ignore")
pd.options.display.max_columns = None
pd.options.display.max_rows = None
