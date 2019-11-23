from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import QuestionBlock, Question, Institution


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'block')
    # podobno tak szybciej
    list_select_related = ('block',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(QuestionBlock)
class QuestionBlockAdmin(admin.ModelAdmin):
    list_display = ('name','_questions')
    inlines = [QuestionInline]
    
    def _questions(self, obj):
        return mark_safe(('<br/><br/>').join([q.name for q in obj.questions.all()]))

admin.site.register(Institution)

