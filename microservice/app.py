from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib
import json
import csv


from models import FeaturesInput, PredictionResult, FeaturesInputAB

app = FastAPI()

target = [
    'premium_purchased',
    'premium_purchased_this_month',
]

ab_results_path = 'ab_results.csv'

# Wczytaj wytrenowany model
nn_model = tf.keras.models.load_model("../models/neural_network.keras")
lr_models = {class_name: joblib.load(
    f'../models/lr_model_{class_name}.joblib') for class_name in target}

scaler = joblib.load('../models/scaler.joblib')

with open('../models/thresholds.json', 'r') as json_file:
    thresholds = json.load(json_file)


def append_to_csv(file_path, data):
    row_to_write = ''.join(map(str, data))

    with open(file_path, 'a', newline='') as csvfile:
        csvfile.write(row_to_write + '\n')


def pred_nn(input_data):
    prediction = nn_model.predict(input_data)
    result = {name: prediction[0][i] > thresholds['nn'][name]
              for i, name in enumerate(target)}
    return result


def pred_lr(input_data):
    result = {}
    for i, name in enumerate(target):
        model = lr_models[name]
        prediction = model.predict(input_data)
        result.update({name: prediction[0] > thresholds['lr'][name]})
    return result


@app.post("/predict/nn", response_model=PredictionResult)
async def predict_nn(features: FeaturesInput):
    try:
        input_data = np.array([features.model_dump().get(
            feature) for feature in features.__annotations__.keys()]).reshape(1, -1)

        input_data = scaler.transform(input_data)
        result = pred_nn(input_data)
        return PredictionResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/lr", response_model=PredictionResult)
def predict_lr(features: FeaturesInput):
    try:
        input_data = np.array([features.model_dump().get(
            feature) for feature in features.__annotations__.keys()]).reshape(1, -1)
        input_data = scaler.transform(input_data)
        result = pred_lr(input_data)
        return PredictionResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ab/", response_model=PredictionResult)
def ab_experiment(features: FeaturesInputAB):
    try:
        user_id = features.user_id
        input_data = np.array([features.model_dump().get(
            feature) for feature in features.__annotations__.keys() if feature != 'user_id']).reshape(1, -1)
        input_data = scaler.transform(input_data)
        if user_id % 2 == 0:
            model = 'lr'
            result = pred_lr(input_data)
        else:
            model = 'nn'
            result = pred_nn(input_data)
        line = f'{model},{user_id},{int(result[target[0]])},{int(result[target[1]])}'
        append_to_csv(ab_results_path, line)
        return PredictionResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/reset/')
def reset():
    columns = ['model', 'user_id', 'premium_purchased',
               'premium_purchased_this_month']
    with open(ab_results_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(columns)
