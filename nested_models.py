# when we started using one model as field for another model then it is called nested model
from pydantic import BaseModel

# make a pydantic model for address
class Address(BaseModel):
    city: str
    state: str  
    pin: str

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address

address_dict={'city':'Guwahati', 'state':'Assam', 'pin':'781001'}
#object for address model
address1=Address(**address_dict)

patient_dict={'name':'Ananya Verma', 'age':28, 'gender':'female', 'address':address_dict}

patient1=Patient(**patient_dict)

print(patient1.name)
print(patient1.age)
print(patient1.gender)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.pin)

# Better organization of related data (e.g.  vitals, address , insurance)
# Reusability : Use Vitals in miltiple models (e.g., Patient, MedicalRecord)
# Readibility: Easier for developers and API consumers to understand
# Validation: Nested models are validated automatically- no extra work needed.