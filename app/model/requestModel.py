from pydantic import BaseModel, Field, field_validator
import re



class libraryModel(BaseModel):
    bookId   : str
    memberId : str