from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: int,
        published_date: int,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(description="Year of publication", gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Author's name",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2020,
            }
        }
    }


BOOKS: list[Book] = [
    Book(
        id=1,
        title="Computer Science Pro",
        author="CodingwithPrince",
        description="A very nice book",
        rating=1,
        published_date=2012,
    ),
    Book(
        id=1,
        title="Master DSA",
        author="CodingwithPrince",
        description="A very nice book",
        rating=2,
        published_date=2022,
    ),
    Book(
        id=2,
        title="Master System Design",
        author="CodingwithPrince",
        description="A very nice book",
        rating=5,
        published_date=2024,
    ),
    Book(
        id=3,
        title="Computer Mathematics Pro",
        author="CodingwithPrince",
        description="A very nice book",
        rating=4,
        published_date=2024,
    ),
    Book(
        id=4,
        title="Call of Sampson",
        author="CodingwithPrince",
        description="An interesting book",
        rating=5,
        published_date=2024,
    ),
    Book(
        id=5,
        title="CyberSecurity Pro",
        author="CodingwithPrince",
        description="A very detailed book",
        rating=5,
        published_date=2024,
    ),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Resource not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return: list = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return BOOKS


@app.put("/books/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed: bool = False
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book.id:
            BOOKS[index] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed: bool = False
    for i in range(len(BOOKS) - 1):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return: list = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published_date == published_date:
            books_to_return.append(BOOKS[i])
    return books_to_return


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
