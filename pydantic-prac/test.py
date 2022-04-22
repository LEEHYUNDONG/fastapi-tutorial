from pydantic import BaseModel, Field, validator

class User(BaseModel):
    name : str = Field(..., regex=r'^[a-zA-Z0-9]*$')
    password : str
    age:int = Field(..., gt=0, le=100)
    
    class Config:
        allow_mutation = False
    
    # @validator("age") # 재사용시 reuse
    # def age_validation(cls, value):
    #     if value < 80:
    #         setattr(cls, "age_brac", "Age under 80")


user = User(name="leerer", password="lll123123", age=10)

# print(user.age_brac)
print(user.dict())

# user.name="leerfee!$" 
# print(type(user.name))
