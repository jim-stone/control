from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView

from .models import Control, Question, QuestionBlock, Checklist, QuestionInList,\
     Institution, QuestionInControl, Answer

from .forms import SearchQuestionForm, AddQuestionToListForm, AddControlForm, AddAnswerToQuestionForm


class IndexView(View):
    def get(self, request):
        return render(request, 'kontrolBack/index.html')


# lista pytań
class QuestionListView(LoginRequiredMixin,ListView):
    model = Question
    context_object_name = 'questions'
    queryset = Question.objects.all().order_by('block__name', 'name')
    paginate_by = 10


# wyszukiwanie pytań
class SearchQuestionView(LoginRequiredMixin, FormView):
    form_class = SearchQuestionForm
    template_name = 'kontrolBack/question_search.html'
    ctx = {} 
    def get(self, request):
        query = self.request.GET.get('search_input')
        
        print (self.request.__dict__)
        if not query is None:
            if query != '':
                print ('query: ', query)
                questions = Question.objects.filter(name__icontains=query)
                self.ctx['questions'] = questions
                if not questions:
                    self.ctx['not_found_message'] = "Nie znaleziono pytań zawierających szukany tekst."
            else:
                questions = Question.objects.all()
                self.ctx['questions'] = questions
            self.ctx['header'] = f'Wyniki wyszukiwania dla <{query}>'
            query = None
        return render(request, self.template_name, self.ctx)


# lista wzorów checklist
class ChecklistListView(LoginRequiredMixin, ListView):
    model = Checklist    
    context_object_name = 'checklists'
    queryset = Checklist.objects.all().order_by('-created_at')
    paginate_by = 150


# tworzy wzór checklisty
class ChecklistAddView(LoginRequiredMixin, CreateView):
    model = Checklist
    fields = ['name']
    success_url = 'listy'


# ogląd checklisty
class ChecklistDetailViewSimplified(LoginRequiredMixin, DetailView):
    model = Checklist
    fields = ['name', 'questions']
    context_object_name = 'checklist'
    template_name = 'kontrolBack/checklist_detail_simple.html'


# edycja checklisty
class ChecklistEditView(LoginRequiredMixin, View):

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

            qs_to_create = [
                QuestionInList.objects.create(question_name=q, block_name=block) for q in questions
                ]

            # print(questions)
            # print(qs_to_create)

            try:
                # dziwna walidacja
                qs_for_checklist = list(checklist.questions.values_list('question_name', flat=True))
                for new_q in qs_to_create:
                    print(new_q.question_name.name, 'in??', qs_for_checklist)
                    assert new_q.question_name.name not in qs_for_checklist

                # koniec dziwnej walidacji
                checklist.questions.add(*qs_to_create)
                messages.success (request, "Zapisano zmiany.")
            except Exception as e:
                messages.error(request, "Coś się nie zgadza. Prawdopodobnie \
                    próbujesz dodać do listy pytanie, które już na niej jest.") 
                print(e)
            # print ([q.checklist.name for q in QuestionInList.objects.all()])
            finally:
                form = AddQuestionToListForm() # to załatwia problem błędnego odświeżania widoku po zapisaniu!!!

        ctx['checklist'] = checklist
        questions = checklist.questions.all().order_by('block_name') # zmienna questions znaczy już zupełnie co innego!
        ctx['questions'] = questions
        ctx['form'] = form
        # ctx['msg'] = msg

        return render(request, 'kontrolBack/checklist_detail.html', ctx)




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

    def form_valid(self, form):
        control = form.save(commit=False)
        control.save()
        for q in control.checklist.questions.all():
            QuestionInControl.objects.create(
                question_name = q.question_name,
                block_name = q.block_name,
                control = control
            )
        messages.success(self.request, 'Kontrola została dodana.')
        return super().form_valid(form)


    
# lista kontroli
class ControlListView (LoginRequiredMixin, ListView):
    context_object_name = 'controls'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Control.objects.all()
        else:
            user_institution = self.request.user.institutionemployee.institution
            return Control.objects.filter(controlling=user_institution)



    

# widok usuwania pytanie z listy sprawdzająceh
def delete_checklist_question (request, checklist_pk, question_pk):
    object = QuestionInList.objects.get(pk=question_pk)
    object.delete()
    return redirect(to='checklist_edit', pk=checklist_pk)

def delete_control (request, pk):
    object = Control.objects.get(pk=pk)
    object.delete()
    return redirect(to='control_list')




class ControlEditView(LoginRequiredMixin, UpdateView):
    model = Control
    fields = 'name project controlling date_start date_end  status'.split()
    context_object_name = 'control'
    template_name = 'kontrolBack/control_detail.html'
    success_url = '/kontrole/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Zmiany zostały zapisane.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Aby zapisać zmiany wypełnij prawidłowo formularz.')
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect ('login')


# przeglądanie wypełnionej checklisty dla controli
class ControlChecklistView(LoginRequiredMixin, View):

    def get(self, request, pk):
        ctx = {}
        control = Control.objects.get(pk=pk)
        questions = control.questions.order_by('block_name')
        # print ([q.pk for q in questions])
        ctx['control'] = control
        ctx['questions'] = questions
        return render(request, 'kontrolBack/ControlChecklist.html', ctx)

# edycja checklisty
# widok na razie "pusty", główna funkcjonalność w AnswerAddView
class ControlChecklistEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # przyjmuje control.id
        ctx = {}
        control = Control.objects.get(pk=pk)
        questions = control.questions.order_by('block_name')
        # form = AddQuestionToListForm()
        ctx['control'] = control
        ctx['questions'] = questions
        # ctx['form'] = form
        return render(request, 'kontrolBack/ControlChecklistEdit.html', ctx)


class AnswerAddView(LoginRequiredMixin, View):
 
    def get (self, request, question_pk):
        question = QuestionInControl.objects.get(pk=question_pk)
        form = AddAnswerToQuestionForm()
        ctx = {'question': question, 'form': form}
        return render(request, 'kontrolBack/AddAnswer.html', ctx)
    
    def post(self, request, question_pk):
        question = QuestionInControl.objects.get(pk=question_pk)
        form = AddAnswerToQuestionForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = form.cleaned_data['comment']
            Answer.objects.create(
                question=question,
                content=content,
                comment=comment
            )
        return redirect(to='control_checklist', pk=question.control.pk)

class AnswerEditView(LoginRequiredMixin, UpdateView):
    form_class = AddAnswerToQuestionForm
    template_name = 'kontrolBack/AddAnswer.html'
