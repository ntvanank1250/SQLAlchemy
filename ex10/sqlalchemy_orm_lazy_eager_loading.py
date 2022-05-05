import os
from sqlalchemy.orm import joinedload, selectinload
import data.db_session as db_session
from data.publisher import Publisher
from data.book import Book
from data.book_details import BookDetails
from data.author import Author
from data.BookAuthor import BookAuthor


def setup_db():
    db_file=os.path.join(os.path.dirname(__file__), 'db', 'Bookstore.sqlite')
    db_session.global_init(db_file)

def create_publisher(name):
    publisher=Publisher()
    publisher.name=name
    return publisher

def create_book(title, isbn, pages, publisher):
    book=Book()
    book.title=title
    book.isbn=isbn
    book.pages=pages
    book.publisher=publisher
    return book

def create_author(first, last):
    author=Author()
    author.first_name=first
    author.last_name=last
    return author

def create_book_details(cover, book):
    details=BookDetails()
    details.book=book
    details.cover=cover
    return details

def create_publisher_with_3_books(ses):
    manning= create_publisher("Manning Publications")
    ses.add(manning)

    #one to many
    bookA=create_book("The Olds", "152604116522",245, manning)
    ses.add(bookA)

    bookB = create_book('Three idiots', "123654222122", 249, manning)
    ses.add(bookB)

    bookC = create_book('parasite', "123654222122", 352, manning)
    ses.add(bookC)

    #many to many
    authorA=create_author('duy-hiu','do')
    ses.add(authorA)
    authorB=create_author('van-hau','nguyen')
    ses.add(authorB)
    authorC=create_author('khi-toa','van')
    ses.add(authorC)

    bookA.authors.append(authorA)
    bookB.authors.append(authorB)
    bookC.authors.append(authorC)

    #one to one
    ses.commit()
    return manning.id

def lazy_loading_works_while_session_open(publisher_id, ses):
    publisher=ses.query(Publisher).filter(Publisher.id==publisher_id).first()
    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t{book}:")
        for author in book.authors:
            print(f"\t\t{author}")

def lazy_loading_throws_error(publisher_id, ses):
    publisher=ses.query(Publisher).filter(Publisher.id== publisher_id).first()

    print(f"{publisher}:")

    for book in publisher.books:
        print(f"\t{book}:")
        for author in book.authors:
            print(f"\t\t{author}")

def eager_loading_joinedload(publisher_id,ses):
    publisher=ses.query(Publisher).options(joinedload("books").joinedload("authors")).\
        filter(Publisher.id==publisher_id).first()

    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t {book}:")
        for author in book.authors:
            print(f"\t\t{author}")

def eager_loading_selectinload(publisher_id,ses):
    publisher=ses.query(Publisher).options(selectinload("books").selectinload("authors")).\
        filter(Publisher.id==publisher_id).first()

    print(f"{publisher}:")
    for book in publisher.books:
        print(f"\t {book}:")
        for author in book.authors:
            print(f"\t\t{author}")
        

if __name__=='__main__':
    print("\n--- setup_db()---\n")
    setup_db()

    print("\n--- create session---\n")
    session=db_session.factory()

    print("\n--- create_publisher_with_3_books() ---\n")
    publisher_id= create_publisher_with_3_books(session)


    print("\n--- lazy_loading_works_while_session_open()---\n")
    lazy_loading_works_while_session_open(publisher_id, session)

    print("\n--- lazy_loading_throws_error()---\n")
    try:
        lazy_loading_throws_error(publisher_id, session)
    except Exception as error:
        print(f"{type(error)}:{error}")

    print("\n--- eager_loading_joinedload()---\n")
    eager_loading_joinedload(publisher_id, session)

    print("\n--- eager_loading_selectinload()---\n")
    eager_loading_selectinload(publisher_id, session)

    print("--- close session---")
    session.close



