from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


control_status = [
    (0, 'w przygotowaniu'),
    (1, 'w trakcie'),
    (2, 'w procesie zgłaszania uwag do wyniku'),
    (3, 'zakończona'),
]

answer_choices = [
    (0, 'tak'),
    (1, 'nie'),
    (2, 'nie dotyczy')
]


class Institution (models.Model):
    name = models.CharField(max_length=512, unique=True)

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

class InstitutionEmployee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    institution = models.ForeignKey(to=Institution, on_delete=models.CASCADE)


class ProjectParticipant(models.Model):
    name = models.CharField(max_length=512)
    def __str__(self):
        return self.name

class Project(models.Model):
    code = models.CharField(max_length=512, unique=True)
    name = models.CharField(max_length=512)
    value = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    description = models.CharField(max_length=3000, null=True)
    beneficiary = models.ForeignKey(to=ProjectParticipant, related_name='projects_as_benef', on_delete=models.PROTECT)
    partners = models.ManyToManyField(to=ProjectParticipant, related_name='projects_as_partner') 

    def __str__(self):
        return self.code



class QuestionBlock (models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


class Question (models.Model):
    name = models.CharField(max_length=500, unique=True)
    block = models.ForeignKey(to=QuestionBlock, related_name='questions', on_delete=models.DO_NOTHING)

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


# założenie: 1 checklista do 1 kontroli w 1 podmiocie

class Checklist(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self,*args,**kwargs):
        return reverse('checklist_detail',kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Control (models.Model):
    name = models.CharField(max_length=2000)
    subject = models.CharField(max_length=2000)
    project = models.ForeignKey(to=Project, related_name="controls_at_project", on_delete=models.PROTECT) 
    controlling = models.ForeignKey(to=Institution, related_name="controls_by", on_delete=models.DO_NOTHING)
    controlled = models.ForeignKey(to=ProjectParticipant, related_name="controls_at_participant", on_delete=models.DO_NOTHING)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    checklist = models.ForeignKey(to=Checklist, null=True, on_delete=models.SET_NULL, related_name='controls')
    status = models.IntegerField(choices=control_status, default=0)


# pytanie wybrane do listy jest dla niej "mrożone"
# tj. nie zmienia się po zmianie pytania bazowego w modelu Question
# i tak samo jest z blokiem

class QuestionInList (models.Model):
    question_name = models.CharField(max_length=500)
    block_name = models.CharField(max_length=255)
    checklist = models.ForeignKey(to=Checklist, related_name='questions', on_delete=models.CASCADE)
    answer = models.IntegerField(choices=answer_choices, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question_name', 'checklist'],
            name="dont_repeat_question_in_checklist")
        ]


class ResultInfo (models.Model):
    control = models.OneToOneField(to=Control, on_delete=models.PROTECT)

class Finding(models.Model):
    result_info = models.ForeignKey(to=ResultInfo, related_name='findings', on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)

class Recommendation (models.Model):
    result_info = models.ForeignKey(to=ResultInfo, related_name='recommendations', on_delete=models.PROTECT)
    content = models.CharField(max_length=10000)


class Comment (models.Model):
    question = models.ForeignKey(to=QuestionInList, on_delete=models.DO_NOTHING, related_name='comments')
    checklist = models.ForeignKey(to=Checklist, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        unique_together = ('question', 'checklist',)

















