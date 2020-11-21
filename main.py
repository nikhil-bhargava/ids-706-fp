from flask import Flask, request, render_template, session, redirect
import os
from pathlib import Path
import pandas as pd
app = Flask(__name__)

repo_path = Path(os.getcwd())
df = pd.read_csv(repo_path / 'data' / '07_model_output' / 'output.csv')
df = df.rename(columns={'style_code':'Style Code', 'name': 'Sneaker Name', 'date':'Date', 
                        'retail_price':'Retail', 'pred_resale_price':'Predicted Resale'})

@app.route('/', methods=("POST", "GET"))
def sneaker_table():
    return render_template('resale_template.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    # return render_template("resale_template2.html", column_names=df.columns.values, row_data=list(df.values.tolist()),link_column="Style Code", zip=zip)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    # app.run()