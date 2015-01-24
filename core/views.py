from django.shortcuts import render
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'core/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published books."""
        return ''
