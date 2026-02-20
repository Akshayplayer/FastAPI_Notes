
from schema.user_input import UserInput
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse


app = FastAPI()

@app.get('/')
def home():
    return {"message":"Insurance premium predictor API"}


#Adding a healthcheckup API for AWS to check the health of the API and it is running or not
@app.get('/health')
def healthcheck():
    return {"status": "ok",
            "version": MODEL_VERSION,
            "model": model is not None 
            }

@app.post('/predict',response_model=PredictionResponse)
def predict_premium(data: UserInput): # provide data from user input type to the model

    # create a pandas  dataframe as our model works on dataframes
    user={
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict_output(user)

        return JSONResponse(status_code=200, content={'predicted_category': prediction})

    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})




