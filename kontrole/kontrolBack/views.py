from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import ListView, CreateView
from .models import Control


class IndexView(View):
    def get(self, request):
        return render(request, 'kontrolBack/index.html')


class ControlAdd(CreateView):
    model = Control
    fields = ['goal', 'subject', 'controlling_institution', 'controlled_institution', 'date_start', 'date_end']
    success_url = 'kontrole'


class ControlListView (ListView):
    model = Control
    context_object_name = 'controls'



