from pydantic import BaseModel
from typing import List, Dict, Optional 

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: Optional[bool]=False  #optional describe that the parameter is optional to be passed
    allergies: Optional[List[str]]=None #List[str] #not to validate that allergies is a list but also that all its elements are strings
    contact_details: Dict[str, str]

patient_info={'name':'Akshay','age':'30', 'weight':'60', 'allergies':['Pollen','Dust'], 'contact_details':{'email':'abc@gmail.com','phone':'1234567890'}}

patient1=Patient(**patient_info)
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print("inserted")

insert_patient_data(patient1)
