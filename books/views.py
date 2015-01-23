from django.shortcuts import render
from django.views import generic

from books.models import CanonicalBook, Author, Publisher


class BookListView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published books."""
        return CanonicalBook.objects.order_by('-pub_date')[:10]
