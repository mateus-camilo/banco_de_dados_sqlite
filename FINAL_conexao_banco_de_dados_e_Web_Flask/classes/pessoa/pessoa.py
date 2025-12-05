from datetime import date
from pydantic import BaseModel

class Pessoa(BaseModel):
    id : int
    nome : str
    data_nascimento : date | str
   