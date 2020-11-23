from flask import Flask, request, render_template, redirect, url_for
from model_resale import predicted_sneaker_resale
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/ResalePredictor')
def ResalePredictor():
    return render_template('ResalePredictor.html')

@app.route('/ResalePredictor', methods=['POST'])
def ResalePredictorPost():
    form_dict = {'name':request.form['SneakerName'], 'brand': request.form['BrandName'], 
                'retail': request.form['RetailPrice'], 'date': request.form['Date'],
                'wmns': request.form['Sex'], 'collab': request.form['Collab'], 'retro': request.form['Retro'],
                'kids': request.form['Kids']}
    final_output = predicted_sneaker_resale(form_dict)
    return render_template('ResalePredictorPost.html', final_output=final_output)

@app.route('/ResaleCalendar', methods=("POST", "GET"))
def ResaleCalendar():
    repo_path = Path(os.getcwd())
    month = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    today = datetime.today()
    current_month = month[today.month]

    df = pd.read_csv(repo_path / 'data' / '07_model_output' / 'output.csv')
    df = df.rename(columns={'style_code':'Style Code', 'name': 'Sneaker Name', 'date':'Date', 
                            'retail_price':'Retail', 'pred_resale_price':'Predicted Resale'})

    return render_template('ResaleCalendar.html',  tables=[df.to_html(classes='data')], titles=df.columns.values, current_month=current_month)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run()
