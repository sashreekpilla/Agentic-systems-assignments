from pydantic import BaseModel, Field, EmailStr, field_validator

class UserRegister(BaseModel):
    username: str = Field(min_length=5)
    email: EmailStr
    age: int = Field(ge=18)

user_register_info = {'username' : 'Sashreek', 'email' : 'Sashreek@email.com', 'age' : 28}
User = UserRegister(**user_register_info)
print(User)