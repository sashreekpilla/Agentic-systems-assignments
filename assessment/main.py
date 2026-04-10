from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from typing import List

app=FastAPI()

class Book (BaseModel):
    title: str = Field(min_length=4)
    author: str = Field(default="Anonomys")
    year:int = Field(gt=1700)

books: List[Book]= []

@app.get("/books")
def get_all_books():
    return books
                                        

@app.post("/books")
def create_book(book: Book):
    books.append(book)
    return book


@app.get("/books/{book_id}")
def search_book(book_id:int):
    
    if book_id<0 or book_id>=len(books):
        raise HTTPException(status_code=404, detail="Book id not found")
    return books[book_id]




Book1=["Harry Potter","J K Rowling",1900]
create_book(Book1)
Book2=["The Alchemist","Paulo Coelho",1988]
create_book(Book2)
Book3=["The Da Vinci Code","Dan Brown",2003]
create_book(Book3)

get_all_books()

search_book(2)
