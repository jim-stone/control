from django import forms
from .models import QuestionBlock, Question

class AddQuestionToListForm(forms.Form):
    
    choices_blocks = [('', '--------------------')] + [(b.pk, b.name) for b in QuestionBlock.objects.all()]
    choices_questions = [(q.pk, q.name) for q in Question.objects.all()]
    block = forms.ChoiceField(choices=choices_blocks)
    questions = forms.ChoiceField(choices=choices_questions, widget=forms.CheckboxSelectMultiple())

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['questions'].queryset = Question.objects.none()
    #     print(self.fields['questions'].queryset)
