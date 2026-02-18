from pydantic import BaseModel, field_validator, Field
import re
class MakeAPIKey(BaseModel):
    name:str = Field(...,min_length=6,max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(n:str)->str:
        if not re.fullmatch(r"[\w -]+", n):
            raise ValueError("Name can only contain letters, numbers, spaces, hyphens, and underscores")
        return n
#used regex syntax or regular expression