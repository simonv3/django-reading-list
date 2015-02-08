import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from readers.models import Reader


class ReaderAPITests(APITestCase):
    """
    Tests for the reader API endpoints.
    """
    def setUp(self):
        self.reader = Reader.objects.create(name='Test Publisher')

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
