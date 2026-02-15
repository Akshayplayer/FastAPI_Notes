from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json
app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data 

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', example='P001')]

    name: Annotated[str, Field(..., description='Name of the patient')]

    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]    
    gender: Annotated[Literal['male', 'female','others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field # computed_field is used to create a new field based on existing fields
    @property # property is used to create a new field based on existing fields
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi>=18.5 and self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']],Field(default=None)]
    height: Annotated[Optional[float],Field(default=None, gt=0)]
    weight: Annotated[Optional[float],Field(default=None, gt=0)]
        
@app.post('/create')
def create_patient(patient:Patient):

    #load the existing data
    data=load_data()

    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    #new patient added to the database.
    data[patient.id]=patient.model_dump(exclude=[id])

    #save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient created successfully'}) 


@app.put('/update/{patient_id}')
def update_patient(patient_id:str, patient_update:PatientUpdate): # in the input it will receive a path parameter and a request body for updating the data.
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info=data[patient_id]

    updated_patient_info=patient_update.model_dump(exclude_unset=True) #the .model_dump() method is used to convert a pydantic model into a dictionary. The exclude_unset parameter is used to exclude fields that are not set in the request body.

    # from the updated patient info, update the existing patient info
    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value

    
    #existing_patient_info-> pydantic model -> when we convert it into pydantic model then it will also calculate bmi and verdict   
    existing_patient_info['id']=patient_id
    patient_pydantic_model=Patient(**existing_patient_info)

    # again we convert it into a dictionary
    existing_patient_info=patient_pydantic_model.model_dump(exclude='id')

    #update the data
    data[patient_id]=existing_patient_info

    #save into json file
    save_data(data)

    #return the response
    return JSONResponse(status_code=200, content={'message':'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        JSONResponse(status_code=404, content={'message':'Patient not found'})
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Patient deleted successfully'})