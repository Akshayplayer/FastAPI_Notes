from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field# Field is used to apply custom validators
from typing import List, Dict, Optional, Annotated  # Annotated is use to attach metadata when use with Field

# Field validators help in adding custom validations as well as transformations.
class Patient(BaseModel):
    name: str
    Email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    

    @computed_field # computed_field is used to create a new field based on existing fields
    @property # property is used to create a new field based on existing fields
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi


patient_info={'name':'Akshay','Email':'abc@icici.com','age':'90', 'weight':90.90,'height':1.80,'married':True, 'allergies':['Pollen','Dust'], 'contact_details':{'email':'abc@hdfc.com','phone':'1234567890'}}

patient1=Patient(**patient_info) # both "validation" and "type cersion" happens in this part of the code
# Type coercion is the automatic or implicit conversion of values from one data type to another (e.g., string to number, object to boolean) performed by a programming language engine, most notably JavaScript, during operations. It allows different data types to interact, such as 1 + "2" resulting in "12."


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.Email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print('BMI:',patient.bmi)
    print("inserted")

insert_patient_data(patient1)