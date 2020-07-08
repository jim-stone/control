from django.shortcuts import render, reverse, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.views.generic import ListView, CreateView, DetailView,\
    UpdateView, FormView
from .models import Control, Question, QuestionBlock, Checklist,\
    QuestionInList, Institution, QuestionInControl, Answer, Project

from .forms import SearchQuestionForm, AddQuestionToListForm,\
    AddControlForm, AddAnswerToQuestionForm
from .mixins import user_has_perm_to_object


class IndexView(View):
    def get(self, request):
        return render(request, 'kontrolBack/index.html')


# lista pytań
class QuestionListView(LoginRequiredMixin, ListView):
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
        if query is not None:
            if query != '':
                questions = Question.objects.filter(name__icontains=query)
                self.ctx['questions'] = questions
                if not questions:
                    self.ctx['not_found_message'] = "Nie znaleziono pytań zawierających szukany tekst."
            else:
                questions = Question.objects.all()
                self.ctx['questions'] = questions
            self.ctx['header'] = f'Wyniki wyszukiwania dla "{query}"'
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

    def form_valid(self, form):
        checklist = form.save(commit=False)
        checklist.created_by = self.request.user.institutionemployee
        checklist.save()
        messages.success(
            self.request, 'Nowa lista sprawdzająca została utworzona.')
        return super().form_valid(form)


# ogląd checklisty
class ChecklistDetailViewSimplified(LoginRequiredMixin, DetailView):
    model = Checklist
    fields = ['name', 'questions']
    context_object_name = 'checklist'
    template_name = 'kontrolBack/checklist_detail_simple.html'


# edycja checklisty
class ChecklistEditView(LoginRequiredMixin, View):

    def get(self, request, pk):
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
            block = QuestionBlock.objects.get(
                pk=int(form.cleaned_data.get('block')))
            questions = Question.objects.filter(
                pk__in=(form.cleaned_data.get('questions')))

            qs_to_create = [
                QuestionInList.objects.create(question_name=q, block_name=block) for q in questions
            ]

            try:
                # dziwna walidacja
                qs_for_checklist = list(
                    checklist.questions.values_list('question_name', flat=True))
                for new_q in qs_to_create:
                    assert new_q.question_name.name not in qs_for_checklist
                # koniec dziwnej walidacji

                checklist.questions.add(*qs_to_create)
                messages.success(request, "Zapisano zmiany.")
            except Exception:
                messages.error(request, "Coś się nie zgadza. Prawdopodobnie \
                    próbujesz dodać do listy pytanie, które już na niej jest.")
            finally:
                # to załatwia problem błędnego odświeżania widoku po zapisaniu!!!
                form = AddQuestionToListForm()

        ctx['checklist'] = checklist
        # zmienna questions znaczy już zupełnie co innego!
        questions = checklist.questions.all().order_by('block_name')
        ctx['questions'] = questions
        ctx['form'] = form
        # ctx['msg'] = msg

        return render(request, 'kontrolBack/checklist_detail.html', ctx)


# tworzy kontrolę
class ControlAdd(LoginRequiredMixin, CreateView):
    form_class = AddControlForm
    success_url = 'kontrole'
    template_name = 'kontrolBack/control_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get(self, request, *args, **kwargs):
        user_institution = Institution.objects.filter(
            pk=self.request.user.institutionemployee.institution.pk)
        user_programme = user_institution[0].programme
        accessible_projects = Project.objects.filter(programme=user_programme)
        form = AddControlForm(initial={'controlling': user_institution[0]})
        form.fields['controlling'].queryset = user_institution
        form.fields['project'].queryset = accessible_projects

        accessible_checklists = Checklist.objects.filter(
            created_by__institution__programme=user_programme
        )
        form.fields['checklist'].queryset = accessible_checklists

        project_titles = list(
            accessible_projects.values_list('name', flat=True))
        project_ids = list(accessible_projects.values_list('pk', flat=True))
        projects = [{'label': z[0], 'value':z[1]}
                    for z in zip(project_titles, project_ids)]

        return render(request, self.template_name, {
            'form': form, 'projects': projects})

    def form_valid(self, form):
        control = form.save(commit=False)
        control.save()
        for q in control.checklist.questions.all():
            QuestionInControl.objects.create(
                question_name=q.question_name,
                block_name=q.block_name,
                control=control
            )
        messages.success(self.request, 'Kontrola została dodana.')
        return super().form_valid(form)


# lista kontroli
class ControlListView(LoginRequiredMixin, ListView):
    context_object_name = 'controls'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Control.objects.all()
        else:
            user_institution = self.request.user.institutionemployee.institution
            return Control.objects.filter(controlling=user_institution)


# widok usuwania pytanie z listy sprawdzająceh
def delete_checklist_question(request, checklist_pk, question_pk):
    object = QuestionInList.objects.get(pk=question_pk)
    object.delete()
    return redirect(to='checklist_edit', pk=checklist_pk)


def delete_control(request, pk):
    object = Control.objects.get(pk=pk)
    object.delete()
    return redirect(to='control_list')


def delete_checklist(request, pk):
    object = Checklist.objects.get(pk=pk)
    try:
        object.delete()
        return redirect(to='checklist_list')
    except ProtectedError:
        messages.error(
            request, "Lista została użyta w co najmniej jednej kontroli. Aby usunąć listę należy najpierw usunąć jej powiązania z kontrolami.")
        return redirect(to='checklist_detail', pk=pk)


def delete_answer(request, pk):
    object = Answer.objects.get(pk=pk)
    control = object.question.control
    object.delete()
    return redirect(to='control_checklist', pk=control.pk)


class ControlEditView(LoginRequiredMixin, UpdateView):
    model = Control
    context_object_name = 'control'
    template_name = 'kontrolBack/control_detail.html'
    success_url = '/kontrole/'
    form_class = AddControlForm

    def render_to_response(self, context, **response_kwargs):
        if not user_has_perm_to_object(self.request.user, self.object):
            return HttpResponse('Brak uprawnień. Ten projekt jest realizowany w innym programie.', status=401)
        return super().render_to_response(context, **response_kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        print(kwargs)
        ctx = super().get_context_data(**kwargs)
        user_institution = Institution.objects.filter(
            pk=self.request.user.institutionemployee.institution.pk)
        user_programme = user_institution[0].programme
        accessible_projects = Project.objects.filter(programme=user_programme)
        project_titles = list(
            accessible_projects.values_list('name', flat=True))
        project_ids = list(accessible_projects.values_list('pk', flat=True))
        projects = [{'label': z[0], 'value':z[1]}
                    for z in zip(project_titles, project_ids)]
        ctx['projects'] = projects
        return ctx

    def form_valid(self, form):
        new_control = form.save(commit=False)
        old_control = Control.objects.get(pk=new_control.pk)

        # czy można tak hakować...
        if new_control.checklist != old_control.checklist:
            if new_control.status != 0:
                msg = 'Nie można zmienić listy sprawdzającej dla kontroli o statusie innym niż w "przygotowaniu".'
                messages.error(self.request, msg)
                return super().form_invalid(form)
            try:
                new_control.questions.all().delete()
            except ProtectedError:
                msg = '''Nie można zmienić listy sprawdzającej ponieważ udzielono już odpowiedzi na niektóre pytania.
                <br>Możesz spróbować usunąć najpierw te odpowiedzi.'''
                messages.error(self.request, msg)
                return super().form_invalid(form)

            new_control.save()
            for q in new_control.checklist.questions.all():
                QuestionInControl.objects.create(
                    question_name=q.question_name,
                    block_name=q.block_name,
                    control=new_control
                )

        # new_control.save()
        messages.success(self.request, 'Zmiany zostały zapisane.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.fields['date_start'].__dict__)
        messages.error(
            self.request, 'Aby zapisać zmiany wypełnij prawidłowo formularz.')
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('login')


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
        ctx['control'] = control
        ctx['questions'] = questions
        return render(request, 'kontrolBack/ControlChecklistEdit.html', ctx)


class AnswerAddView(LoginRequiredMixin, View):

    def get(self, request, question_pk):
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

    model = Answer
    form_class = AddAnswerToQuestionForm
    template_name = 'kontrolBack/EditAnswer.html'

    def get_success_url(self):
        pk = self.object.question.control.pk
        return reverse('control_checklist', kwargs={'pk': pk})
