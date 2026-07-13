

from fastapi import FastAPI
from pydantic import BaseModel
from routinglogic.plan import plan_trip
from fastapi.middleware.cors import CORSMiddleware\


app=FastAPI()
origins = [
    "*",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,    
    allow_methods=["*"],        
    allow_headers=["*"],        
)
class Data(BaseModel):
    start:str
    end:str



@app.post("/find/")
def home(data: Data):
    start = data.start
    end = data.end
    if start=="" or end=="":
        return {"message":"no data sent"}
    
    # Remove 'await' if find_buse is a normal function
    result = plan_trip(start,end)
    
    return result   
