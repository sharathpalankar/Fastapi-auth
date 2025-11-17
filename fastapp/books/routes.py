from typing import List ,Optional
from fastapi import APIRouter,Depends,status
from .schemas import Book
from .service import BookService
from db import database
from dependencies import RoleChecker

def get_books_collection():
    return database['books']

book=BookService()

book_router =APIRouter()
@book_router.get("/books/",status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_books(books_collection=Depends(get_books_collection),depends_role: dict = Depends(RoleChecker(allowed_roles=["user", "admin"]))):
    book_records=await BookService.get_all_books(books_collection)
    return book_records

@book_router.get("/books/{book_id}",status_code=status.HTTP_200_OK, response_model=Optional[Book])
async def get_book_by_id(book_id: str, books_collection=Depends(get_books_collection),depends_role: dict = Depends(RoleChecker(allowed_roles=["user", "admin"]))):
    book_record = await BookService.get_book_by_id(books_collection, book_id)
    return book_record
