from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini import generate
from app.services.web_scraping import scraping

router = APIRouter()


class Book(BaseModel):
    title: List[str]

@router.post("/books")
def list_book(book: Book):
    return scraping(book.title)
     

@router.post("/books/info")
def get_book_info(book: Book):
    return generate(book.title)

@router.post("/books/pdf")
def get_book_pdf(book: Book):
    return null


