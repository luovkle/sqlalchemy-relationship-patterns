from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///one_to_one.db")
SessionLocal = sessionmaker(engine)

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    book = relationship(
        "Book", back_populates="author", uselist=False, cascade="all, delete"
    )

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    title = Column(String(64), nullable=False, unique=True)
    author = relationship("Author", back_populates="book", uselist=False)

    def __init__(self, author_id: int, title: str) -> None:
        self.author_id = author_id
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
    book_1 = Book(noah.id, "Five weeks in a balloon")
    book_2 = Book(lucas.id, "The mysterious island")
    book_3 = Book(mia.id, "The horror of Dunwich")

    db.add_all([book_1, book_2, book_3])
    db.commit()

    print(f"{noah.name}: {noah.book}")
    print(f"{mia.name}: {mia.book}")
    print(f"{lucas.name}: {lucas.book}\n")

    print(f"{book_1.title}: {book_1.author}")
    print(f"{book_3.title}: {book_3.author}")
    print(f"{book_2.title}: {book_2.author}")
