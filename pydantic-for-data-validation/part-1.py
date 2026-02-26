from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError

class UserRegister(BaseModel):
    username: str = Field(min_length=5)
    email: EmailStr
    age: int = Field(ge=18)

try:
    user_register_info = {'username' : 'Sashreek', 'email' : 'Sashreek@email.com', 'age' : 20}
    User = UserRegister(**user_register_info)
    print(User)

except ValidationError as e:
    print(e)
