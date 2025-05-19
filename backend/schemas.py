from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
  login: str
  password: str
  firstname: str
  secondname: str


class UserLogin(BaseModel):
  login: str
  password: str


class ChangePasswordSchema(BaseModel):
  old_password: str
  new_password: str


class TicketSchema(BaseModel):
  title: str
  description: str


class CommentSchema(BaseModel):
  text: str


class UserOutSchema(BaseModel):
  id: int
  login: str
  firstname: str
  secondname: str
  role: str

  class Config:
    orm_mode = True

class CommentOutSchema(BaseModel):
  id: int
  text: str
  author_id: int
  created_on: datetime
  ticket_id: int

  class Config:
    orm_mode = True

class FullCommentOutSchema(BaseModel):
  id: int
  text: str
  author: UserOutSchema
  created_on: datetime
  ticket_id: int

  class Config:
    orm_mode = True

class TicketOutSchema(BaseModel):
  id: int
  title: str
  description: str
  created_on: datetime
  updated_on: datetime
  author: UserOutSchema
  assignee: Optional[UserOutSchema] = None
  
  class Config:
    orm_mode = True

class FullTicketOutSchema(BaseModel):
  id: int
  title: str
  description: str
  created_on: datetime
  updated_on: datetime
  author: UserOutSchema
  assignee_id: Optional[UserOutSchema] = None
  comments: List[FullCommentOutSchema]

  class Config:
    orm_mode = True
