from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Data Models
class Book(BaseModel):
    id: int
    title: str
    author: str
    available: bool = True

class Member(BaseModel):
    id: int
    name: str
    email: str

class Checkout(BaseModel):
    id: int
    book_id: int
    member_id: int
    checkout_date: datetime
    return_date: Optional[datetime] = None

# In-memory DB
books: List[Book] = []
members: List[Member] = []
checkouts: List[Checkout] = []

# --- Home ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Books ---

@app.get("/books", response_class=HTMLResponse)
async def list_books(request: Request):
    return templates.TemplateResponse("books.html", {"request": request, "books": books})

@app.get("/books/add", response_class=HTMLResponse)
async def add_book_form(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@app.post("/books/add", response_class=HTMLResponse)
async def add_book(request: Request, id: int = Form(...), title: str = Form(...), author: str = Form(...)):
    if any(b.id == id for b in books):
        return templates.TemplateResponse("add_book.html", {"request": request, "error": "Book ID already exists"})
    new_book = Book(id=id, title=title, author=author, available=True)
    books.append(new_book)
    return RedirectResponse(url="/books", status_code=303)

@app.get("/books/delete/{book_id}", response_class=HTMLResponse)
async def delete_book(request: Request, book_id: int):
    global books
    books = [b for b in books if b.id != book_id]
    return RedirectResponse(url="/books", status_code=303)

# --- Members ---

@app.get("/members", response_class=HTMLResponse)
async def list_members(request: Request):
    return templates.TemplateResponse("members.html", {"request": request, "members": members})

@app.get("/members/add", response_class=HTMLResponse)
async def add_member_form(request: Request):
    return templates.TemplateResponse("add_member.html", {"request": request})

@app.post("/members/add", response_class=HTMLResponse)
async def add_member(request: Request, id: int = Form(...), name: str = Form(...), email: str = Form(...)):
    if any(m.id == id for m in members):
        return templates.TemplateResponse("add_member.html", {"request": request, "error": "Member ID already exists"})
    new_member = Member(id=id, name=name, email=email)
    members.append(new_member)
    return RedirectResponse(url="/members", status_code=303)

@app.get("/members/delete/{member_id}", response_class=HTMLResponse)
async def delete_member(request: Request, member_id: int):
    global members
    members = [m for m in members if m.id != member_id]
    return RedirectResponse(url="/members", status_code=303)

# --- Checkouts ---

@app.get("/checkouts", response_class=HTMLResponse)
async def list_checkouts(request: Request):
    # Include book and member info for display
    detailed_checkouts = []
    for c in checkouts:
        book = next((b for b in books if b.id == c.book_id), None)
        member = next((m for m in members if m.id == c.member_id), None)
        detailed_checkouts.append({
            "checkout": c,
            "book": book,
            "member": member,
        })
    return templates.TemplateResponse("checkouts.html", {"request": request, "checkouts": detailed_checkouts})

@app.get("/checkouts/add", response_class=HTMLResponse)
async def add_checkout_form(request: Request):
    available_books = [b for b in books if b.available]
    return templates.TemplateResponse("add_checkout.html", {"request": request, "books": available_books, "members": members})

@app.post("/checkouts/add", response_class=HTMLResponse)
async def add_checkout(request: Request, book_id: int = Form(...), member_id: int = Form(...)):
    book = next((b for b in books if b.id == book_id), None)
    if not book or not book.available:
        return templates.TemplateResponse("add_checkout.html", {"request": request, "error": "Book not available", "books": [b for b in books if b.available], "members": members})

    member = next((m for m in members if m.id == member_id), None)
    if not member:
        return templates.TemplateResponse("add_checkout.html", {"request": request, "error": "Member not found", "books": [b for b in books if b.available], "members": members})

    book.available = False
    checkout_id = len(checkouts) + 1
    new_checkout = Checkout(id=checkout_id, book_id=book_id, member_id=member_id, checkout_date=datetime.utcnow())
    checkouts.append(new_checkout)
    return RedirectResponse(url="/checkouts", status_code=303)

@app.get("/checkouts/return/{checkout_id}", response_class=HTMLResponse)
async def return_checkout(request: Request, checkout_id: int):
    checkout = next((c for c in checkouts if c.id == checkout_id), None)
    if checkout and checkout.return_date is None:
        book = next((b for b in books if b.id == checkout.book_id), None)
        if book:
            book.available = True
        checkout.return_date = datetime.utcnow()
    return RedirectResponse(url="/checkouts", status_code=303)
