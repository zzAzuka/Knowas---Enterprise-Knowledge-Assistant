from pydantic import BaseModel

class uploadOutput(BaseModel):
    filename: str
    status: str
    message: str