from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError, ConfigDict

class User(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    age: int = Field(ge=18)
    address: Address
    is_premium: bool = Field(default= False)

    model_config=ConfigDict(validate_assignment=True)

class Address(BaseModel):
    city: str = Field(min_length=3)
    pincode: str = Field(min_length=6, max_length=6)

    @field_validator("pincode")
    def check_digits(cls, v):
        if not v.isdigit():
            raise ValueError("pincode must be digits")
        return v

    model_config=ConfigDict(validate_assignment=True)


try:
    address= {'city':'hyd', 'pincode':'abcdef'}
    user = {'user_id':'45','name' : 'Sashreek', 'email' : 'sashreek@gmail.com', 'age' : 20, 'address':address, 'is_premium':'0'}
    User1 = User(**user)
    print(User1)

except ValidationError as e:
    print(e)
