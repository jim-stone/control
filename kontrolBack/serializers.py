from rest_framework import serializers
from .models import Question, QuestionBlock, Institution


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'name', 'block']


class QuestionBlockSerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True)
    # js assumes question is not serialized here

    class Meta:
        model = QuestionBlock
        fields = ['id', 'name', 'questions']


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
