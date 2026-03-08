from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI()


#simple API endpoint to return JSON
@app.get("/hello")
def hello():
    return {"message" : "Hello, Welcome to FastAPI!"}


#middleware function
@app.middleware("http")
async def first_middleware(request: Request, call_next):

    print("Message before the request is processed")
   
    response = await call_next(request)

    print("Message after the request is processed")

    print ("Path:", request.url.path)
    print ("Method:",request.method)

    return response


#custom 404 exception handler for undefined routes
@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "The requested resource was not found."
        }
    )
