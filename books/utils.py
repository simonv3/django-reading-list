import json

from books.models import Book, Author, Edition, Publisher, BookExtra


def process_isbndb_result(result):
    """
    Inputs the results from isbndb, and returns the related pks
    """
    books = []
    for data in result['data']:
        book = find_book_by_isbn(data['isbn13'], data['isbn10'])
        if book:
            # It exists so append
            books.append(book.pk)
        else:
            authors, names = find_authors(data['author_data'])

            # If the author exists, check that there is no author /
            # title combination for this book. If there is, it means
            # that this is probably a different edition.
            same, book = find_same_book_by_title_and_name(data['title'], names)
            if book:
                # book exists, let's assume it's a new edition.
                # (we've already confirmed that the isbn10/13 doesn't exist)
                create_edition(book, data)
            else:
                # book doesn't exist yet. Let's create it, the edition,
                # and the relevant extras.
                book = Book.objects.create(
                    title=data['title'],
                    sub_title=data['title_long']
                    )
                book.authors = authors
                book.save()
                create_edition(book, data)
            books.append(book.pk)
    return books


def find_book_by_isbn(isbn13, isbn10):
    """
    Search for the book first by isbn13 if there
    is one. Else by isbn10.
    """
    book = Book.objects.get_or_none(
        editions__extras__key='isbn13',
        editions__extras__val_char=isbn13)

    if not book:
        book = Book.objects.get_or_none(
            editions__extras__key='isbn10',
            editions__extras__val_char=isbn10)

    return book


def find_authors(author_data):
    """
    Loop through the names and stop assuming they're western.
    """
    author_names = []
    for author in author_data:
        name = author['name']
        if ',' in name:
            name = ' '.join([x.strip() for x in name.split(',')][::-1])
        # Check that the author exists
        Author.objects.get_or_create(name=name)
        author_names.append(name)
    authors = Author.objects.filter(name__in=author_names)
    return authors, author_names


def find_same_book_by_title_and_name(title, names):
    """
    Loop through all the books matching the title and return
    the one who has the same authors.
    """
    books = Book.objects.filter(title=title)
    for book in books:
        same = 0
        for author in book.authors.all():
            if author.name in names:
                same += 1

        if same == len(names):
            return True, book
    return False, None


def create_edition(book, data):
    publisher, created = Publisher.objects.get_or_create(
        name=data['publisher_name'])

    edition = Edition.objects.create(
        book=book,
        publisher=publisher)

    create_extra(edition, 'isbn13', data['isbn13'])
    create_extra(edition, 'isbn10', data['isbn10'])
    create_extra(edition, 'dewey_decimal', data['dewey_decimal'])
    create_extra(edition, 'language', data['language'])
    create_extra(edition, 'summary', data['summary'])
    edition.save()
    return edition


def create_extra(edition, key, extra):
    """
    Check if the extra exists and add it if it does
    """
    if extra:
        if extra is 'summary':
            BookExtra.objects.create(
                book=edition,
                key=key,
                val_text=extra)
        else:
            BookExtra.objects.create(
                book=edition,
                key=key,
                val_char=extra)
