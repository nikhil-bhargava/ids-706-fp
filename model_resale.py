import os
from pathlib import Path
import pandas as pd
import numpy as np
from statsmodels.iolib.smpickle import load_pickle
import statsmodels.formula.api as smf

def predicted_sneaker_resale(form_dict):

    repo_path = Path(os.getcwd())
    lm = load_pickle(repo_path / "prod-models" / "resale_predictor.pickle")
    try:
        df = pd.DataFrame(form_dict, index=[0])
        df['retail'] = df['retail'].astype(int)
        df['log_retail'] = np.log(df['retail'])
        df['date'] = pd.to_datetime(df['date'])
        df['release_month'] = df['date'].dt.month
        df['release_dow'] = df['date'].dt.weekday
        month = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        dow = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
        df['release_month'] = df['release_month'].map(month)
        df['release_dow'] = df['release_dow'].map(dow)

        wmns = {'Male':0, 'Female':1}
        df['wmns'] = df['wmns'].map(wmns)

        bools = {'No':0, 'Yes':1}
        df['collab'] = df['collab'].map(bools)
        df['retro'] = df['retro'].map(bools)
        df['kids'] = df['kids'].map(bools)

        sname = form_dict['name']
        pred_resale_price = round(np.exp(lm.predict(df)[0]))
        retail = int(form_dict['retail'])
        diff = round(pred_resale_price - retail)
        pp = round(((pred_resale_price - retail) / pred_resale_price)*100, 2)

        return "The {0} is expected to resell for ${1}! This is a projected {2} dollar difference from the original ${4} retail price and an {3}% price premium.".format(sname, pred_resale_price, diff, pp, retail)

    except:
        return 'Sorry, there was a problem processing the data entered... Please go back and double check your entries, thanks!'