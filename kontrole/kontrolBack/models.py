from django.db import models

control_status = [
    (0, 'w przygotowaniu'),
    (1, 'w trakcie'),
    (2, 'zakończona'),
]

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


class Institution (models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name

# założenie: 1 checklista do 1 kontroli

class Checklist(models.Model):
    questions = models.ManyToManyField(to=Question)


class Control (models.Model):
    goal = models.CharField(max_length=2000)
    subject = models.CharField(max_length=2000)
    controlling_institution = models.ForeignKey(to=Institution, related_name="controls_by", on_delete=models.DO_NOTHING)
    controlled_institution = models.ForeignKey(to=Institution, related_name="controls_at", on_delete=models.DO_NOTHING)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    checklist = models.ForeignKey(to=Checklist, null=True, on_delete=models.SET_NULL, related_name='controls')
    status = models.IntegerField(choices=control_status)


class ResultInfo (models.Model):
    control = models.OneToOneField(to=Control, on_delete=models.CASCADE)


class Recommendation (models.Model):
    result_info = models.ForeignKey(to=ResultInfo, related_name='recommendations', on_delete=models.CASCADE)


class Comment (models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.DO_NOTHING, related_name='comments')
    checklist = models.ForeignKey(to=Checklist, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        unique_together = ('question', 'checklist',)

















