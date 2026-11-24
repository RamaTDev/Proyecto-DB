


from pydantic import BaseModel


class Category(BaseModel):

    categoryid : int

    categoryname : str

    description: str

    picture: str

    discontinued: bool


class CategoryCreate(BaseModel):

    categoryname : str

    description: str

    picture: str



class CategoryID(BaseModel):

    categoryid: int
