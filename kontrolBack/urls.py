from django.conf.urls import url
from rest_framework import routers
from .api import QuestionViewSet, QuestionBlockViewSet, InstitutionViewSet
from .views import IndexView, ControlAdd, ControlListView,\
    QuestionListView, ChecklistAddView, ChecklistListView,\
    ChecklistEditView, delete_checklist_question, delete_control, ControlEditView,\
    SearchQuestionView, ChecklistDetailViewSimplified, ControlChecklistEditView,\
    ControlChecklistView, AnswerAddView, AnswerEditView, delete_checklist, delete_answer

router = routers.DefaultRouter()

# REST API viewsets
router.register(r'questions', QuestionViewSet, 'questions')
router.register(r'blocks', QuestionBlockViewSet, 'blocks')
router.register(r'institutions', InstitutionViewSet, 'institutions')


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^index', IndexView.as_view(), name='index'),
    url(r'^dodaj_kontrole', ControlAdd.as_view(), name='control_add'),
    url(r'^kontrole/(?P<pk>\d+)$', ControlEditView.as_view(), name='control_edit'),
    url(r'^kontrole/$', ControlListView.as_view(), name='control_list'),
    url(r'^szukaj_pytania', SearchQuestionView.as_view(), name='question_search'),
    url(r'^pytania$', QuestionListView.as_view(), name='question_list'),
    url(r'^dodaj_liste', ChecklistAddView.as_view(), name='checklist_add'),
    url(r'^listy/(?P<pk>\d+)/$', ChecklistDetailViewSimplified.as_view(),
        name='checklist_detail'),
    url(r'^edycja_listy/(?P<pk>\d+)/$',
        ChecklistEditView.as_view(), name='checklist_edit'),
    url(r'^listy$', ChecklistListView.as_view(), name='checklist_list'),
    url(r'^delete/(?P<pk>\d+)$', delete_checklist, name='checklist_delete'),
    url(r'^delete/(?P<checklist_pk>\d+)/(?P<question_pk>\d+)/$',
        delete_checklist_question, name='checklist_question_delete_view'),
    url(r'^kontrole/(?P<pk>\d+)/lista$',
        ControlChecklistView.as_view(), name='control_checklist'),
    url(r'^kontrole/(?P<pk>\d+)/lista/edycja',
        ControlChecklistEditView.as_view(), name='control_checklist_edit'),
    url(r'^kontrole/delete/(?P<pk>\d+)/', delete_control, name='control_delete'),
    url(r'^kontrole/dodaj_odpowiedz/(?P<question_pk>\d+)/$',
        AnswerAddView.as_view(), name='answer_add'),
    url(r'^kontrole/edytuj_odpowiedz/(?P<pk>\d+)/$',
        AnswerEditView.as_view(), name='answer_edit'),
    url(r'^kontrole/usun_odpowiedz/(?P<pk>\d+)/$',
        delete_answer, name='answer_delete'),

]
