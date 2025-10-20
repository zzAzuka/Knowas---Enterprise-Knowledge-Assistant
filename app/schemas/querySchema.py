from pydantic import BaseModel

class queryInput(BaseModel):
    query: str

class queryOutput(BaseModel):
    response: str