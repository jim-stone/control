from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from .models import Control, Question, QuestionBlock, Checklist, QuestionInList
from .forms import AddQuestionToListForm
from django.http import HttpResponse

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


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    queryset = Question.objects.all().order_by('block__name', 'name')
    paginate_by = 150


class ChecklistAddView(CreateView):
    model = Checklist
    fields = ['name']
    success_url = 'listy'

    

class ChecklistListView(ListView):
    model = Checklist    
    context_object_name = 'checklists'
    queryset = Checklist.objects.all().order_by('name')
    paginate_by = 150

class ChecklistDetailView(View):
    # model = Checklist
    # context_object_name = 'checklist'
    # template_name = 'kontrolBack/checklist_detail.html'

    def get (self, request, pk):
        ctx = {}
        checklist = Checklist.objects.get(pk=pk)
        form = AddQuestionToListForm()
        ctx['checklist'] = checklist
        print(checklist.questions.all())
        ctx['form'] = form
        return render(request, 'kontrolBack/checklist_detail.html', ctx)

    def post(self, request, pk):
        ctx = {}
        checklist = Checklist.objects.get(pk=pk)
        form = AddQuestionToListForm(request.POST)
        if form.is_valid():
            block = QuestionBlock.objects.get(pk = int(form.cleaned_data.get('block')))
            questions = Question.objects.filter(pk__in=(form.cleaned_data.get('questions')))
            objs_to_create = [
                QuestionInList(question_name=q, block_name=block, checklist=checklist)\
                    for q in questions
                ]
            QuestionInList.objects.bulk_create(objs_to_create)
            print ([q.checklist.name for q in QuestionInList.objects.all()])

        return render(request, 'kontrolBack/checklist_detail.html', ctx)
        # return HttpResponse ('Done')









