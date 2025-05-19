from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  login = Column(String, unique=True)
  firstname = Column(String)
  secondname = Column(String)
  hashed_password = Column(String)
  role = Column(String, default='user')

  comments = relationship('Comment', back_populates='author')


class Ticket(Base):
  __tablename__ = 'tickets'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  description = Column(String)
  created_on = Column(DateTime, default=datetime.utcnow)
  updated_on = Column(DateTime, default=datetime.utcnow)
  author_id = Column(Integer, ForeignKey('users.id'))
  assignee_id = Column(Integer, ForeignKey('users.id'))

  author = relationship('User', foreign_keys=[author_id])
  assignee = relationship('User', foreign_keys=[assignee_id])
  comments = relationship('Comment', back_populates='ticket')


class Comment(Base):
  __tablename__ = 'comments'

  id = Column(Integer, primary_key=True)
  text = Column(String)
  author_id = Column(Integer, ForeignKey('users.id'))
  created_on = Column(DateTime, default=datetime.utcnow)
  ticket_id = Column(Integer, ForeignKey('tickets.id'))

  author = relationship('User', back_populates='comments')
  ticket = relationship('Ticket', back_populates='comments')
