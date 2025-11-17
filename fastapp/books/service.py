from bson import ObjectId
import secrets

class BookService:
    # @staticmethod
    async def get_all_books(books_collection):
        books = []
        async for book in books_collection.find():
            book['_id'] = str(book['_id'])  # Convert ObjectId to string
            books.append(book)
        return books
    
    async def get_book_by_id(books_collection, book_id: str):
        obj_id= ObjectId(book_id)
        book = await books_collection.find_one({"_id": (obj_id)})
        print(book,"book in service",obj_id)
        if book:
            book['_id'] = str(book['_i d'])  # Convert ObjectId to string
        return book
    
    # async def createBook()

