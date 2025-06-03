from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime

# Books
def get_books(db: Session):
    return db.query(models.Book).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Members
def get_members(db: Session):
    return db.query(models.Member).all()

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# Checkouts
def get_checkouts(db: Session):
    return db.query(models.Checkout).all()

def create_checkout(db: Session, checkout: schemas.CheckoutCreate):
    db_checkout = models.Checkout(**checkout.dict())
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout

def return_book(db: Session, checkout_id: int):
    db_checkout = db.query(models.Checkout).filter(models.Checkout.id == checkout_id).first()
    if db_checkout:
        db_checkout.return_date = datetime.utcnow()
        db.commit()
        db.refresh(db_checkout)
    return db_checkout
