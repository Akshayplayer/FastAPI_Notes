from fastapi import FastAPI, Path, HTTPException, Query #import fastapi
import json

app=FastAPI() # create a FastAPI object

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

@app.get("/") # create a decorator function
def root():
    return {"message": "Hello World"}

@app.get('/about')
def about():
    return {"message": "About Page"}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(..., description='ID of the patient in the DB', example='P001')): #... means that the parameter is required
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of Height, Weight or BMI'), order: str = Query('asc', description='sort in Asc or desc order')):
    valid_orders=['height','weight','bmi']
    if sort_by not in  valid_orders:
        raise HTTPException(status_code=400, detail='Invalid sort_by parameter')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order parameter')
    
    data=load_data()
    order_by=True if order=='desc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=order_by)
    return sorted_data