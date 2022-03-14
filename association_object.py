from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///association_object.db")
SessionLocal = sessionmaker(engine)

Base = declarative_base()


class AuthorBook(Base):
    __tablename__ = "author_books"

    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    author = relationship("Author", back_populates="books")
    book = relationship("Book", back_populates="authors")

    def __init__(self, author_id: int, book_id: int) -> None:
        self.author_id = author_id
        self.book_id = book_id

    def __repr(self) -> str:
        return f"<AuthorBook {self.author_id} {self.book_id}>"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    books = relationship("AuthorBook", back_populates="author")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)
    authors = relationship("AuthorBook", back_populates="book")

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

    # AuthorBook
    author_book1 = AuthorBook(noah.id, book_1.id)
    author_book2 = AuthorBook(noah.id, book_2.id)
    author_book3 = AuthorBook(mia.id, book_1.id)
    author_book4 = AuthorBook(mia.id, book_3.id)
    author_book5 = AuthorBook(lucas.id, book_2.id)
    author_book6 = AuthorBook(lucas.id, book_3.id)

    db.add_all(
        [
            author_book1,
            author_book2,
            author_book3,
            author_book4,
            author_book5,
            author_book6,
        ]
    )
    db.commit()

    # Print relationships between authors and books
    authors = [noah, mia, lucas]
    for author in authors:
        print(f"{author.name}:")
        for book in author.books:
            print(f"\t{book.book.title}")

    print("\n")

    books = [book_1, book_2, book_3]
    for book in books:
        print(f"{book.title}:")
        for author in book.authors:
            print(f"\t{author.author.name}")
