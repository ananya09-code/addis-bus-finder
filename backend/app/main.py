

from fastapi import FastAPI
from pydantic import BaseModel
from routinglogic.find_rote import find_buse
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
    
    # Remove 'await' if find_buse is a normal function
    result = find_buse(start, end) 
    
    return result   
