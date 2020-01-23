from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import QuestionBlock, Question, Institution, InstitutionEmployee


class InstitutionEmployeeInline(admin.StackedInline):
    model = InstitutionEmployee
    can_delete = False
    verbose_name_plural = 'employees'


class UserAdmin(BaseUserAdmin):
    inlines = (InstitutionEmployeeInline,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'order_in_block', 'is_active')
    # podobno tak szybciej
    list_select_related = ('block',)
    # readonly_fields = ('name', 'block', 'order_in_block', 'is_replacement_for')


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
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
