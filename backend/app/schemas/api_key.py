from pydantic import BaseModel, field_validator, Field
import re
class MakeAPIKey(BaseModel):
    name:str = Field(...,min_length=6,max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, n:str)->str:
        if not re.fullmatch(r"[\w -]+", n):
            raise ValueError("Name can only contain letters, numbers, spaces, hyphens, and underscores")
        return n
    

'''Missing cls Argument: A @field_validator is a class method. Its first argument must be the class (cls), and the second is the value (v).

ncorrect Decorator Order: If you use @classmethod, it must be placed below the @field_validator decorator'''