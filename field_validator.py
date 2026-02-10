from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator# Field is used to apply custom validators
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

    #Field validator for validating fields
    @field_validator('Email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com']
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f'Invalid domain name {domain_name}')
        return value
    
    #Field validator for transformation (convert every name to uppercase)
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
    # when mode is before type coersion happens after validation that mean if validation fails then type coersion will not happen
    
    @field_validator('age', mode='before')
    @classmethod
    def check_age(cls,value):
        if value<18:
            raise ValueError('Age should be greater than 18')
        return value
    

    # In case we wanted to validate multiple fields at a time then we use model_validator instead of field_validator
    


patient_info={'name':'Akshay','Email':'abc@icici.com','age':30, 'weight':90.90,'married':True, 'allergies':['Pollen','Dust'], 'contact_details':{'email':'abc@hdfc.com','phone':'1234567890'}}

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