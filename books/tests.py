import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book, Author, Publisher


class BookAPITests(APITestCase):
    """
    Tests for the book API endpoints.
    """
    def setUp(self):
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.author = Author.objects.create(name='Test Author')

    def test_create_book_succeeds(self):
        """
        Ensure we can create a new book object.
        """
        url = reverse('book-list')
        data = {
            'title': 'A Test Book Title',
            'sub_title': 'A Test Book Title',
            'isbn_13': '0123456789123',
            'published': datetime.date.today(),
            'authors': [self.author.id],
            'publisher': self.publisher.id
            }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(Book.objects.all().first().title, data['title'])

    def test_delete_book_succeeds(self):
        """
        Ensure we can delete a book object.
        """

        data = {
            'title': 'A Test Book Title',
            'sub_title': 'A Test Book Title',
            'isbn_13': '0123456789123',
            'published': datetime.date.today(),
            'publisher': self.publisher
        }

        book = Book.objects.create(**data)
        book.authors.add(self.author)

        url = reverse('book-detail', args=(book.id,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_partial_update_book_succeeds(self):
        """
        Ensure we can update a book object.
        """

        data = {
            'title': 'Updated Title',
            'sub_title': 'A Test Book Title',
            'isbn_13': '0123456789123',
            'published': datetime.date.today(),
            'publisher': self.publisher
        }

        book = Book.objects.create(**data)
        book.authors.add(self.author)

        url = reverse('book-detail', args=(book.id,))
        response = self.client.patch(url, {'title': 'Patched Title',
                                           'sub_title': 'New'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Book.objects.all().first().title, 'Patched Title')
        self.assertEqual(Book.objects.all().first().sub_title, 'New')

    def test_update_book_succeeds(self):
        """
        Ensure we can update a book object.
        """

        data = {
            'title': 'Updated Title',
            'sub_title': 'A Test Book Title',
            'isbn_13': '0123456789123',
            'published': datetime.date.today(),
            'publisher': self.publisher
        }

        book = Book.objects.create(**data)
        book.authors.add(self.author)
        new_publisher = Publisher.objects.create(name='Heyo')
        url = reverse('book-detail', args=(book.id,))
        response = self.client.put(url, {'title': 'Updated Title'
                                         'sub_title': 'New Sub',
                                         'isbn_13': '1234567891234',
                                         'publisher': new_publisher,
                                         'published': datetime.date.today()})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Book.objects.all().first().title, 'Updated Title')
        self.assertEqual(Book.objects.all().first().isbn_13, '1234567891234')
