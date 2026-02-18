from pydantic import BaseModel,EmailStr,field_validator, Field

class CreateUser(BaseModel):
    email:EmailStr
    password:str = Field(...,min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(p:str)->str:
        if not any(char.isalpha() for char in p):
            raise ValueError("Password must contain at least one letter")
        if not any(char.isdigit() for char in p):
            raise ValueError("Password must contain at least one number")
        return p