from pydantic import BaseModel,model_validator
import uuid
from datetime import datetime, date

class Book(BaseModel):
    title: str
    author: str
    description: str
    page_count: int
    language: str

class BookCreateModel(BaseModel):
    title: str
    author: str
    description: str 
    page_count: int
    published_year: int
    language: str

    @model_validator(mode='before')
    def validate_page_count(cls, values):
        page_count = values.get('page_count')
        if page_count is not None and page_count <= 20:
            raise ValueError("Page count must be greater than 20")
        return values
    # def validate_page_count(self):
    #     if self.page_count <= 20:
    #         raise ValueError("Page count must be a greater than 20")
    #     return self.page_count

class BookUpdateModel(BaseModel):
    title: str 
    author: str 
    description: str
    page_count: int 
    language: str     