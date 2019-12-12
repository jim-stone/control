from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Control, Question, QuestionBlock, Checklist, QuestionInList
from .forms import AddQuestionToListForm


class IndexView(View):
    def get(self, request):
        return render(request, 'kontrolBack/index.html')


class ControlAdd(LoginRequiredMixin, CreateView):
    model = Control
    fields = ['goal', 'subject', 'controlling_institution', 'controlled_institution', 'date_start', 'date_end', 'checklist']
    success_url = 'kontrole'


class ControlListView (LoginRequiredMixin, ListView):
    # model = Control
    context_object_name = 'controls'

    def get_queryset(self):
        user_institution = self.request.user.institutionemployee.institution
        return Control.objects.filter(controlling=user_institution)



class QuestionListView(LoginRequiredMixin,ListView):
    model = Question
    context_object_name = 'questions'
    queryset = Question.objects.all().order_by('block__name', 'name')
    paginate_by = 5


class ChecklistAddView(LoginRequiredMixin, CreateView):
    model = Checklist
    fields = ['name']
    success_url = 'listy'

    

class ChecklistListView(LoginRequiredMixin, ListView):
    model = Checklist    
    context_object_name = 'checklists'
    queryset = Checklist.objects.all().order_by('-created')
    paginate_by = 150

class ChecklistDetailView(LoginRequiredMixin, View):
    # model = Checklist
    # context_object_name = 'checklist'
    # template_name = 'kontrolBack/checklist_detail.html'

    def get (self, request, pk):
        ctx = {}
        checklist = Checklist.objects.get(pk=pk)
        questions = checklist.questions.all().order_by('block_name')
        form = AddQuestionToListForm()
        ctx['checklist'] = checklist
        ctx['questions'] = questions
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
            try:    
                QuestionInList.objects.bulk_create(objs_to_create)
                messages.success (request, "Zapisano zmiany.")
            except Exception as e:
                messages.error(request, "Coś się nie zgadza. Prawdopodobnie \
                    próbujesz dodać do listy pytanie, które już na niej jest.") 
            # print ([q.checklist.name for q in QuestionInList.objects.all()])
            finally:
                form = AddQuestionToListForm() # to załatwia problem błędnego odświeżania widoku po zapisaniu!!!

        ctx['checklist'] = checklist
        questions = checklist.questions.all().order_by('block_name') # zmienna questions znaczy już zupełnie co innego!
        ctx['questions'] = questions
        ctx['form'] = form
        # ctx['msg'] = msg

        return render(request, 'kontrolBack/checklist_detail.html', ctx)
    

# widok usuwania pytanie z listy sprawdzająceh
def delete_checklist_question (request, checklist_pk, question_pk):
    object = QuestionInList.objects.get(pk=question_pk)
    object.delete()
    return redirect(to='checklist_detail', pk=checklist_pk)


class ControlEditView(LoginRequiredMixin, UpdateView):
    model = Control
    fields = '__all__'
    context_object_name = 'control'
    template_name = 'kontrolBack/control_detail.html'
    # success_url = reverse_lazy ('control_list')


def logout_view(request):
    logout(request)
    return redirect ('login')
