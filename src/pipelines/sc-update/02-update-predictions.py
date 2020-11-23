# import packages
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np
import os
from pathlib import Path
from statsmodels.iolib.smpickle import load_pickle

# create paths
cur_dir = os.getcwd()
dpath = Path(cur_dir)
dpath = dpath / ".." / ".." / "data" / "02_intermediate"
mpath = dpath / ".." / ".." / "prod-models"

# load test data abd format
test = pd.read_csv(dpath / 'test.csv')
test['wmns'] = test['wmns'].astype('int')
test['collab'] = test['collab'].astype('int')
test['retro'] = test['retro'].astype('int')
test['kids'] = test['kids'].astype('int')
test['log_resale'] = np.log(test['resale_price'])
test['log_retail'] = np.log(test['retail_price'])
test['retail_price'] = test['retail_price'].astype('int')

# get labels for test set
labels = test[['style_code','name','date','retail_price']]

# load model & make predictions
lm = load_pickle(mpath / "resale_predictor.pickle")
lm_resale = pd.DataFrame(lm.predict(test)).rename(columns={0:'pred_resale_price'})
lm_resale['pred_resale_price'] = np.exp(lm_resale['pred_resale_price']).astype('int')

# create output csv & output data
output = pd.concat([labels, lm_resale], axis=1)
output = output.sort_values(by='date')

opath = dpath / ".." / ".." / "data" / "07_model_output"
output.to_csv(opath / 'output.csv', index=False)

output.to_csv(mpath / 'output.csv', index=False)




