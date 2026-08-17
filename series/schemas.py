from pydantic import BaseModel, Field

class Serie(BaseModel):
    titulo: str
    genero: str
    ano_lancamento: int = Field(gt=1900)
    temporadas: int = Field(gt=0)