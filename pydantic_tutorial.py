from pydantic import BaseModel, EmailStr, AnyUrl, Field # Field is used to apply custom validators
from typing import List, Dict, Optional, Annotated  # Annotated is use to attach metadata when use with Field

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 characters', example=['Akshay','Sachin'])] # so here we are applying both validator and attaching metadata.
    Email: EmailStr
    Linkdin_url: AnyUrl
    age: int
    weight: Annotated[float, Field(gt=0, le=200, strict=True)]# that means I applied a custom validator to check that weight is between 0 and 200
    married: Annotated[Optional[bool], Field(default=False, description='Is the patient is married or not')]
    allergies: Optional[List[str]]=Field(max_length=5) #List[str] #not to validate that allergies is a list but also that all its elements are strings
    contact_details: Dict[str, str]

patient_info={'name':'Akshay','Email':'abc@gmail.com','Linkdin_url':'https://linkedin.com/in/akshay','age':'30', 'weight':90.90, 'allergies':['Pollen','Dust'], 'contact_details':{'email':'abc@gmail.com','phone':'1234567890'}}

patient1=Patient(**patient_info)
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print("inserted")

insert_patient_data(patient1)
