from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()


#Query parameter
#product and review are optional parameters
@app.get("/search")
def search_via_name_age(name: str, age: int, product: str |None=None, Review: str |None=None):
    data={"name": name, "age": age}
    #data returning as json
    return data

