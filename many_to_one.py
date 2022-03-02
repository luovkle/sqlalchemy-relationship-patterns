from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///many_to_one.db")
SessionLocal = sessionmaker(engine)

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    def __init__(self, name: str, book_id: int) -> None:
        self.name = name
        self.book_id = book_id

    def __repr__(self) -> str:
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)
    authors = relationship("Author", backref="books")

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"<Book {self.title}>"


with SessionLocal() as db:
    # Restart database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Books
    book_1 = Book("Five weeks in a balloon")
    book_2 = Book("The mysterious island")
    book_3 = Book("The horror of Dunwich")

    db.add_all([book_1, book_2, book_3])
    db.commit()

    # Authors
    noah = Author("Noah", 1)
    mia = Author("Mia", 1)
    lucas = Author("Lucas", 2)

    db.add_all([noah, mia, lucas])
    db.commit()

    print(f"{book_1.title}: {book_1.authors}")
    print(f"{book_2.title}: {book_2.authors}")
    print(f"{book_3.title}: {book_3.authors}")
