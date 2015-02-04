from django.contrib import admin
from readers.models import Reader, Tag, Save, Timeline


admin.site.register(Save)
admin.site.register(Reader)
admin.site.register(Tag)
admin.site.register(Timeline)
