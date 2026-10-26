from pydantic import BaseModel, Field, ConfigDict
from datetime import date as Date
from typing import Optional, Literal

# User
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Transaction
class TransactionBase(BaseModel):
    title: str
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: Literal["income", "expense"]
    category: str
    date: Date

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    date: Optional[Date] = None

class TransactionResponse(TransactionBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)