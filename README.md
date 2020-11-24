# IDS 706: Predicting Sneaker Resale Values
![images 001](https://user-images.githubusercontent.com/31523376/100053226-94b01980-2ded-11eb-996f-23a5b92cbd7c.jpeg)

## Introduction
According to GQ, the sneaker resale market is valued at around $2 billion dollars, with the potential to reach $6 billion by 2025. Although sneaker prices vary over time, previous analysis done by StockX suggests that resale prices begin to plateau after a “month or two”. The purpose of this project is to deploy a sneaker resale price prediction model through the use of a Flask app. The app has been deployed on Google App Engine (GCP) and through continous delivery using Google Cloud Build. 

**FLASK APPLICATION LINK:** https://sneakairs.uc.r.appspot.com/

**VIDEO INTRODUCTION & DEMO:** https://youtu.be/XZZRA7Ox6hE

![images 002](https://user-images.githubusercontent.com/31523376/100054202-9e3a8100-2def-11eb-8bc4-174126e7405c.jpeg)

## Project Outline & Cloud Architecture
The model was trained on data scraped from Sole Collector and StockX. Additional scrapers can also be found in the notebooks section of this repo. The Flask app is running in continous delivery in the back end thanks to Github and Google cloud build. The training data is stored in Google Cloud Storage, but since other files were relatively small, they were also stored locally. The Flask app was deployed using Google App Engine.
![images 003](https://user-images.githubusercontent.com/31523376/100053751-aba33b80-2dee-11eb-8085-e047e6092932.jpeg)

## Entity Relation Diagram (ERD) | Solecollector x StockX Data
Five data tables were scraped and joined together form Sole Collector and StockX. The star by each variable name indicate features used to train the model. The blue s were variables directly input into the model, the pink stars were variables that features were extracted from, and the yellow star is the response variable. The relationships between the five tables are visualized below.
![images 004](https://user-images.githubusercontent.com/31523376/100053908-02107a00-2def-11eb-8816-97ccf23fbfb4.jpeg)

## Getting Started
If you would like to run the flask app locally, run the commands below.

**Step 1: Clone the repo.**
```
git clone https://github.com/nikhil-bhargava/ids-706-fp.git
```

**Step 2: Navigate your way into the repo.**
```
cd ids-706-fp
```

**Step 3: Run the Makefile to install and/or update requirements.**
```
make
```

**(Optional) Step 4: Update month being displayed by flask app calendar by running the bash file. This is not necessary unless you want the most updated sneaker calendar. Note the model will not update.**
```
bash build-calendar.sh
```

**Step 5: Run the flask app locally by executing main.py.**
```
python3 main.py
```
