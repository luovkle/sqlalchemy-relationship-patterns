from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///many_to_many.db")
SessionLocal = sessionmaker(engine)

Base = declarative_base()

author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id")),
    Column("book_id", ForeignKey("books.id")),
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    books = relationship("Book", secondary=author_book, back_populates="authors")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)
    authors = relationship("Author", secondary=author_book, back_populates="books")

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"<Book {self.title}>"


with SessionLocal() as db:
    # Restart database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Authors
    noah = Author("Noah")
    mia = Author("Mia")
    lucas = Author("Lucas")

    db.add_all([noah, mia, lucas])
    db.commit()

    # Books
    book_1 = Book("Five weeks in a balloon")
    book_2 = Book("The mysterious island")
    book_3 = Book("The horror of Dunwich")

    db.add_all([book_1, book_2, book_3])
    db.commit()

    # The relationship between authors and books is established
    noah.books = [book_1, book_2]
    mia.books = [book_1, book_3]
    lucas.books = [book_2, book_3]

    db.add_all([noah, mia, lucas])
    db.commit()

    # The relationship between authors and books is established
    print(f"{noah.name}: {noah.books}")
    print(f"{mia.name}: {mia.books}")
    print(f"{lucas.name}: {lucas.books}\n")

    print(f"{book_1.title}: {book_1.authors}")
    print(f"{book_2.title}: {book_2.authors}")
    print(f"{book_3.title}: {book_3.authors}")
