from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()


#load customers data from customer.json file
def load_cusotmers_data():
    with open('customer.json','r') as f:
        customers_data = json.load(f)

    return customers_data



#Query parameter
@app.get("/search")
def search_via_name_age(name: str=Query(default='Deepak',description="name to be searched by"), age:int=Query(default=30,description="age to be searched by")):

    data=load_cusotmers_data()

    if name not in data:
        raise HTTPException(status_code=404, detail="Details with given name or age are not found name")
    
    if age not in data:
        raise HTTPException(status_code=404, detail="Details with given name or age are not found age")
    
    
    return data

