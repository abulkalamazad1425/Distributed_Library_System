from typing import List
from fastapi import APIRouter,Depends, HTTPException, status
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schema.book_schema import BookCreate, BookOut, BookListResponse,BookUpdate, BookAvailabilityUpdate, BookAvailabilityResponse
from service.bookService import BookService
 
router = APIRouter(prefix="/api/book" , tags=["book"])
bookService = BookService()
@router.post("",response_model= BookOut)
async def create_book(book:BookCreate,db:AsyncSession = Depends(get_db)):
    try:
        return await bookService.create_book(book,db)
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    

@router.get("",response_model=BookListResponse)
async def get_books_by_search(search : str, db:AsyncSession = Depends(get_db)):
    try:
        books= await bookService.get_books_by_search(search,db)
        if not books:
            raise HTTPException(status_code=404, detail="Book not found")
        number_of_books = len(books)
        bookList = {}
        bookList["books"] = books
        bookList["total"]= number_of_books

        return bookList
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))


@router.get("/{book_id}",response_model=BookOut)
async def get_book_by_id(book_id:int, db:AsyncSession = Depends(get_db)):
    try:
        book= await bookService.get_book_by_id(book_id,db)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    


@router.put("/{book_id}", response_model=BookOut)
async def update_book(book_id: int, book:BookUpdate , db: AsyncSession = Depends(get_db)):
    try:
        updated_book = await bookService.update_book(book_id, book, db)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e)) 
    



@router.patch("/{book_id}/availability", response_model=BookAvailabilityResponse)
async def update_book_availability(book_id: int, book: BookAvailabilityUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_book = await bookService.update_book_availability(book_id, book, db)
        if not updated_book:
            raise HTTPException(status_code=404, detail="Book not found")
        return updated_book
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    

@router.delete("/api/books/{id}")
async def remove_book(id: int, db: AsyncSession = Depends(get_db)):
    try:
        success = await bookService.delete_book(id, db)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
        return "204 No Content"
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))