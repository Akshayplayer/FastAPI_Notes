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

# print(patient1.name)
# print(patient1.age)
# print(patient1.gender)
# print(patient1.address.city)
# print(patient1.address.state)
# print(patient1.address.pin)

temp=patient1.model_dump() # convert a pydantic model into a dictionary.
print (temp)
print(type(temp))

temp2=patient1.model_dump_json() # convert a pydantic model into a json.
print(temp2)
print(type(temp2))

temp3=patient1.model_dump(include=['name','gender']) # only include the 'name' and 'gender' fields in dictionary.
print (temp3)
print(type(temp3))

temp4=patient1.model_dump(exclude=['name','gender']) # inclued every field apart from 'name' and 'gender' fields in dictionary.
print (temp4)
print(type(temp4))

# patient2=Patient(**)
