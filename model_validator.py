from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator# Field is used to apply custom validators
from typing import List, Dict, Optional, Annotated  # Annotated is use to attach metadata when use with Field

# Field validators help in adding custom validations as well as transformations.
class Patient(BaseModel):
    name: str
    Email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    

    # In case we wanted to validate multiple fields at a time then we use model_validator instead of field_validator
    @model_validator(mode='after')  # here we are using model validator so we need not to pass any single value hence we are validating whole model
    def validate_emergency_contact(cls, model): # here model is the whole model to validate
        if model.age>60 and 'emergency'  not in model.contact_details:
            raise ValueError("Emergency contact is required for patients above 60 years of age.")
        return model


patient_info={'name':'Akshay','Email':'abc@icici.com','age':'90', 'weight':90.90,'married':True, 'allergies':['Pollen','Dust'], 'contact_details':{'email':'abc@hdfc.com','phone':'1234567890'}}

patient1=Patient(**patient_info) # both "validation" and "type cersion" happens in this part of the code
# Type coercion is the automatic or implicit conversion of values from one data type to another (e.g., string to number, object to boolean) performed by a programming language engine, most notably JavaScript, during operations. It allows different data types to interact, such as 1 + "2" resulting in "12."


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.Email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print("inserted")

insert_patient_data(patient1)