from flask import Flask, request, render_template, session, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField 
from wtforms.validators import DataRequired
import os
from pathlib import Path
import pandas as pd
import numpy as np
from statsmodels.iolib.smpickle import load_pickle
import statsmodels.formula.api as smf

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'any secret string'


RESALE_HTML = """{% extends "login.html" %}
        <html>
            <body>
                {0}'s resale value is predicted to be ${1}.
            </body>
        </html>
    """

repo_path = Path(os.getcwd())

class model_input(FlaskForm):
    sneaker_name = StringField('Sneaker Name', validators=[DataRequired()])
    brand = SelectField('Brand Name', validators=[DataRequired()], choices=[('1', 'Adidas'), ('2', 'Air Jordan'), ('3', 'Asics'), ('4', 'Converse'), ('5', 'Jordan Brand'), ('6', 'New Balance'), ('7', 'Nike'), ('8', 'Nike Basketball'), ('9', 'Nike Running'), ('10', 'Other Brands'), ('11', 'Puma'), ('12', 'Reebok')])
    retail_price = IntegerField('Retail Price', validators=[DataRequired()])
    release_day = SelectField('Release Day', validators=[DataRequired()], choices=[('1', 'Sunday'), ('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday')])
    release_month = SelectField('Release Month', validators=[DataRequired()], choices=[('1', 'Jan'), ('2', 'Feb') , ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug') , ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')])
    collab = BooleanField('Collab')
    retro = BooleanField('Retro')
    wmns = BooleanField('Wmns')
    kids = BooleanField('Kids')
    submit =  SubmitField('Submit')

@app.route('/')

@app.route('/ResalePredictor')
def ResalePredictor():
    # form = model_input()

    # iname = form.sneaker_name.data
    # ibrand = form.brand.data
    # iretail_price = form.retail_price.data
    # irelease_day = form.release_day.data
    # irelease_month = form.release_month.data
    # icollab = form.collab.data
    # iretro = form.retro.data
    # iwmns = form.wmns.data
    # ikids = form.kids.data

    # # data = {'brand':ibrand, 'log_retail':iretail_price, 'release_dow':irelease_day, 
    # # 'release_month':irelease_month, 'collab':icollab, 'retro':iretro, 'wmns':iwmns, 'retro':iretro,
    # # 'kids':ikids}
    # # data = pd.DataFrame(data)

    # # lm = load_pickle(repo_path / prod-models / "resale_predictor.pickle")
    # # pred_resale_price = round(np.exp(lm.predict(data)[0]))

    # if form.validate_on_submit():
    #     return render_template('results.html', name=name, pred=pred_resale_price)

    return render_template('login.html')

@app.route('/ResalePredictor', methods=['POST'])
def ResalePredictorPost():
    your_pick = request.form['text']
    print(your_pick)
    return render_template('ResalePredictorPost.html', your_pick=your_pick)

# @app.route('/SneakerPredictions')
# def manual_predict():
#     inputs = model_input()
#     return render_template('model_input.html', title='Predict Sneaker Resale Price', form=inputs)

# @app.route('/MonthlyPredictions', methods=("POST", "GET"))
# def sneaker_table():
#     df = pd.read_csv(repo_path / 'data' / '07_model_output' / 'output.csv')
#     df = df.rename(columns={'style_code':'Style Code', 'name': 'Sneaker Name', 'date':'Date', 
#                             'retail_price':'Retail', 'pred_resale_price':'Predicted Resale'})

#     return render_template('resale_template.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    # return render_template("resale_template2.html", column_names=df.columns.values, row_data=list(df.values.tolist()),link_column="Style Code", zip=zip)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run()