from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True

class MemberBase(BaseModel):
    name: str
    email: str

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    class Config:
        orm_mode = True

class CheckoutBase(BaseModel):
    book_id: int
    member_id: int

class CheckoutCreate(CheckoutBase):
    pass

class Checkout(CheckoutBase):
    id: int
    checkout_date: datetime
    return_date: Optional[datetime]
    class Config:
        orm_mode = True
