from fastapi import FastAPI, Body


app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "Math"},
    {"title": "Title Three", "author": "Author Three", "category": "Cybersecurity"},
    {"title": "Title four", "author": "Author four", "category": "Algorithm"},
    {
        "title": "Title Five",
        "author": "Author Five",
        "category": "Information Technology",
    },
    {"title": "Title Six", "author": "Author Six", "category": "History"},
    {"title": "Title Seven", "author": "Author Seven", "category": "Geography"},
    {"title": "Title Eight", "author": "Author Eight", "category": "Astronomy"},
    {"title": "Title Nine", "author": "Author One", "category": "Religion"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_books(book_title: str):
    """path params"""
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    """query params"""
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book


@app.put("/books/update_book")
async def update_book(updated_book: dict[str, str] = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
            return BOOKS[i]


@app.delete("/books/delete_book/{booK_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    return {"message": "okay"}
