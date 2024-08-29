from sqlmodel import Field, SQLModel, Relationship



class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    password: str
    first_name: str = Field(max_length=30, nullable=False)
    last_name: str = Field(max_length=30, nullable=False)
    email: str = Field(unique=True, nullable=False)
    
    def __str__(self):
        return self.username
