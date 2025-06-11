from pydantic import BaseModel
from datetime import datetime

class Review(BaseModel):
    ReviewId:str
    ReviewName:str
    WorkloadId:str
    WorkloadName:str
    Owner:str
    ModifiedOn:datetime
    IsDelete:bool = False