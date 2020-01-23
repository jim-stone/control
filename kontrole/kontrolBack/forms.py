from django import forms
from .models import QuestionBlock, Question, Checklist, Control


class SearchQuestionForm(forms.Form):
    search = forms.TextInput()


class AddQuestionToListForm(forms.Form):
    
    choices_blocks = [('', '--------------------')] + [(b.pk, b.name) for b in QuestionBlock.objects.all()]
    choices_questions = [(q.pk, q.name) for q in Question.objects.all()]
    
    new_checklist_name = forms.CharField(max_length=255)

    block = forms.ChoiceField(choices=choices_blocks, initial='')
    questions = forms.MultipleChoiceField(choices=choices_questions, widget=forms.CheckboxSelectMultiple())

class AddControlForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = ['name', 'project', 'controlling', 'date_start', 'date_end', 'checklist']
        widgets = {
            'project': forms.Select()
        }
    