from django.contrib import admin
from books.models import Book, Edition, BookExtra, Publisher, Author

admin.site.register(Book)
admin.site.register(Edition)
admin.site.register(BookExtra)
admin.site.register(Publisher)
admin.site.register(Author)
