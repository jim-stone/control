from django import forms
from .models import QuestionBlock, Question, Checklist, Control, Project
from .models import QuestionInList, answer_choices, QuestionInControl, Answer, Institution


class SearchQuestionForm(forms.Form):
    search = forms.TextInput()


class AddQuestionToListForm(forms.Form):

    choices_blocks = [('', '--------------------')] + [(b.pk, b.name)
                                                       for b in QuestionBlock.objects.all()]
    choices_questions = [(q.pk, q.name) for q in Question.objects.all()]
    block = forms.ChoiceField(choices=choices_blocks, initial='', label='Blok')
    questions = forms.MultipleChoiceField(
        choices=choices_questions,
        widget=forms.CheckboxSelectMultiple(),
        label='Pytania')


class AddControlForm(forms.ModelForm):

    class Meta:
        model = Control
        fields = ['name', 'project', 'status', 'controlling',
                  'date_start', 'date_end', 'checklist']
        widgets = {
            'project': forms.TextInput()
        }

    date_start = forms.DateField(
        input_formats=['%d.%m.%Y'], label="Początek"
    )

    date_end = forms.DateField(
        input_formats=['%d.%m.%Y'], label="Koniec"
    )

    def __init__(self, *args, **kwargs):

        # do poprawy, podobno niebezpieczne
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            user_institution = Institution.objects.filter(
                pk=self.user.institutionemployee.institution.pk)
            user_programme = user_institution[0].programme
            accessible_projects = Project.objects.filter(
                programme=user_programme)
            accessible_checklists = Checklist.objects.filter(
                created_by__institution__programme=user_programme
            )
            self.fields['controlling'].queryset = user_institution
            self.fields['project'].queryset = accessible_projects
            self.fields['checklist'].queryset = accessible_checklists


class AddAnswerToQuestionForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content', 'comment']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'rows': 5,
                    'cols': 50
                }
            )
        }
