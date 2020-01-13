from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, DetailView, UpdateView

from .models import Control, Question, QuestionBlock, Checklist, QuestionInList, Institution
from .forms import AddQuestionToListForm, AddControlForm


class IndexView(View):
    def get(self, request):
        return render(request, 'kontrolBack/index.html')

# tworzy kontrolę
class ControlAdd(LoginRequiredMixin, CreateView):
    form_class = AddControlForm
    success_url = 'kontrole'
    template_name = 'kontrolBack/control_form.html'
    
    def get(self, request, *args, **kwargs):
        
        if request.user.is_superuser:
            form = AddControlForm()
        else:
            user_institution = Institution.objects.filter(pk=self.request.user.institutionemployee.institution.pk)
            form = AddControlForm(initial={'controlling': user_institution[0]})           
            form.fields['controlling'].queryset = user_institution
            form.fields['controlling'].disabled = True
        return render (request, self.template_name, {'form': form})



    
# lista kontroli
class ControlListView (LoginRequiredMixin, ListView):
    context_object_name = 'controls'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Control.objects.all()
        else:
            user_institution = self.request.user.institutionemployee.institution
            return Control.objects.filter(controlling=user_institution)

# lista pytań
class QuestionListView(LoginRequiredMixin,ListView):
    model = Question
    context_object_name = 'questions'
    queryset = Question.objects.all().order_by('block__name', 'name')
    paginate_by = 5


# tworzy wzór checklisty
class ChecklistAddView(LoginRequiredMixin, CreateView):
    model = Checklist
    fields = ['name']
    success_url = 'listy'

    
# lista wzorów checklist
class ChecklistListView(LoginRequiredMixin, ListView):
    model = Checklist    
    context_object_name = 'checklists'
    queryset = Checklist.objects.all().order_by('-created')
    paginate_by = 150

#
class ChecklistDetailView(LoginRequiredMixin, View):

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

            new_checklist_name = form.cleaned_data.get('new_checklist_name')
            print(1, checklist.name, 2, new_checklist_name)

            objs_to_create = [
                QuestionInList(question_name=q, block_name=block, checklist=checklist)\
                    for q in questions
                ]
            try:    
                if new_checklist_name != checklist.name:
                    checklist.name = new_checklist_name
                    checklist.save()
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
    success_url = 'control_edit'
    
    def form_valid(self, form):
        messages.success(self.request, 'Zmiany zostały zapisane.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Aby zapisać zmiany wypełnij prawidłowo formularz.')
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect ('login')
