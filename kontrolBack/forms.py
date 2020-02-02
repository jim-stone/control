from django import forms
from .models import QuestionBlock, Question, Checklist, Control,\
    QuestionInList, answer_choices, QuestionInControl, Answer


class SearchQuestionForm(forms.Form):
    search = forms.TextInput()


class AddQuestionToListForm(forms.Form):
    
    choices_blocks = [('', '--------------------')] + [(b.pk, b.name) for b in QuestionBlock.objects.all()]
    choices_questions = [(q.pk, q.name) for q in Question.objects.all()]
    
    # new_checklist_name = forms.CharField(max_length=255, initial='')

    block = forms.ChoiceField(choices=choices_blocks, initial='', label='Blok')
    questions = forms.MultipleChoiceField(choices=choices_questions, widget=forms.CheckboxSelectMultiple(),
        label='Pytania')

class AddControlForm(forms.ModelForm):
    
    class Meta:
        model = Control
        fields = ['name', 'project', 'controlling', 'date_start', 'date_end', 'checklist']
        widgets = {
            'project': forms.TextInput()
        }
    
    date_start = forms.DateField(
        input_formats= ['%d/%m/%Y'], label="Początek"
    )

    date_end = forms.DateTimeField(
        input_formats= ['%d/%m/%Y'], label="Koniec"
    )


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