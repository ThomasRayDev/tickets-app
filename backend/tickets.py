from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Ticket, Comment
from schemas import TicketSchema, CommentSchema, TicketOutSchema, FullCommentOutSchema, FullTicketOutSchema
from dependencies import get_current_user
from datetime import datetime
from typing import List


router = APIRouter()


@router.get('/', tags=['Tickets'], response_model = List[TicketOutSchema])
def get_tickets(db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  tickets = None
  if db_user.role == 'admin':
    tickets = db.query(Ticket).all()
  else:
    tickets = db.query(Ticket).filter(Ticket.author_id == db_user.id).all()
  return tickets

@router.post('/', tags=['Tickets'], response_model = TicketOutSchema)
def create_ticket(ticket: TicketSchema, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = Ticket(title=ticket.title, description=ticket.description, author_id=db_user.id)
  db.add(db_ticket)
  db.commit()
  db.refresh(db_ticket)
  return db_ticket

@router.get('/{ticket_id}', tags=['Tickets'], response_model = FullTicketOutSchema)
def get_ticket(ticket_id: int, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  if db_ticket.author_id != db_user.id and db_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permission')
  return db_ticket

@router.put('/{ticket_id}', tags=['Tickets'], response_model = TicketOutSchema)
def update_ticket(ticket_id: int, ticket: TicketSchema, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  if db_ticket.author_id != db_user.id and db_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permission')
  db_ticket.title = ticket.title
  db_ticket.description = ticket.description
  db_ticket.updated_on = datetime.utcnow()
  db.commit()
  db.refresh(db_ticket)
  return db_ticket

@router.delete('/{ticket_id}', tags=['Tickets'])
def delete_ticket(ticket_id: int, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  if db_ticket.author_id != db_user.id and db_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permission')
  db.delete(db_ticket)
  db.commit()
  return { 'detail': 'Ticket deleted', 'success': True }


@router.post('/{ticket_id}/comments', tags=['Tickets'], response_model = FullCommentOutSchema)
def create_comment(comment: CommentSchema, ticket_id: int, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  db_comment = Comment(text=comment.text, author_id=db_user.id, ticket_id=ticket_id)
  db.add(db_comment)
  db.commit()
  db.refresh(db_comment)
  return db_comment

@router.get('/{ticket_id}/comments', tags=['Tickets'], response_model = List[FullCommentOutSchema])
def get_comments(ticket_id: int, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  if db_ticket.author_id != db_user.id and db_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permission')
  return db_ticket.comments

@router.delete('/{ticket_id}/comments/{comment_id}', tags=['Tickets'])
def delete_comment(ticket_id: int, comment_id: int, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
  if not db_comment or not db_comment in db_ticket.comments:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ticket has not this comment')
  if db_comment.author_id != db_user.id and db_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permission')
  db.delete(db_comment)
  db.commit()
  return { 'detail': 'Comment deleted', 'success': True }

@router.put('/{ticket_id}/comments/{comment_id}', tags=['Tickets'], response_model = FullCommentOutSchema)
def update_comment(comment: CommentSchema, ticket_id: int, comment_id: int, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
  if not db_ticket:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket not found')
  db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
  if not db_comment or not db_comment in db_ticket.comments:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Ticket has not this comment')
  if db_comment.author_id != db_user.id and db_user.role != 'admin':
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permission')
  db_comment.text = comment.text
  db.commit()
  db.refresh(db_comment)
  return db_comment
