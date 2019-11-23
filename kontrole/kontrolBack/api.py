from rest_framework import viewsets, permissions
from .models import Question, QuestionBlock, Institution
from .serializers import QuestionSerializer, QuestionBlockSerializer, InstitutionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classer = [
        permissions.AllowAny
    ]


class QuestionBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestionBlock.objects.all()
    serializer_class = QuestionBlockSerializer
    permission_classer = [
        permissions.AllowAny
    ]    

class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classer = [
        permissions.AllowAny
    ]    