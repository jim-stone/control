from django.db import models
from django.shortcuts import reverse

control_status = [
    (0, 'w przygotowaniu'),
    (1, 'w trakcie'),
    (2, 'procedowanie uwag do wyniku'),
    (3, 'zakończona'),
]


class Institution (models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


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


# założenie: 1 checklista do 1 kontroli

class Checklist(models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self,*args,**kwargs):
        return reverse('checklist_detail',kwargs={'pk': self.pk})


class Control (models.Model):
    goal = models.CharField(max_length=2000)
    subject = models.CharField(max_length=2000)
    controlling_institution = models.ForeignKey(to=Institution, related_name="controls_by", on_delete=models.DO_NOTHING)
    controlled_institution = models.ForeignKey(to=Institution, related_name="controls_at", on_delete=models.DO_NOTHING)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question_name', 'checklist'],
            name="dont_repeat_question_in_checklist")
        ]


class ResultInfo (models.Model):
    control = models.OneToOneField(to=Control, on_delete=models.CASCADE)


class Recommendation (models.Model):
    result_info = models.ForeignKey(to=ResultInfo, related_name='recommendations', on_delete=models.CASCADE)


class Comment (models.Model):
    question = models.ForeignKey(to=QuestionInList, on_delete=models.DO_NOTHING, related_name='comments')
    checklist = models.ForeignKey(to=Checklist, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        unique_together = ('question', 'checklist',)

















