from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()


#Query parameter
#product and review are optional parameters
@app.get("/search")
def search_via_name_age(name: str=Query(..., description="Name of the customer"), age: int=Query(..., description="age of the customer"), product: str |None=None, Review: str|None=None):


    # validation of name to have only characters
    if any(char.isdigit() for char in name):
        raise HTTPException(status_code=404,detail="name should not have digits")

    data={"name": name, "age": age}
    #returning data as json
    return data

